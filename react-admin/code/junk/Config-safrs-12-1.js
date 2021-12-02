import config from './Config.json'

const init_Conf = () => {
    if(! "raconf" in localStorage){
        console.log("Init Configuration")
        localStorage.setItem("raconf",JSON.stringify(config))
        window.location.reload()
    }
}

export const get_Conf = () => {

    init_Conf();

    let ls_conf = null
    let result = {}
    const lsc_str = localStorage.getItem("raconf")
    try{
        ls_conf = JSON.parse(lsc_str)
        result = ls_conf ? ls_conf : JSON.parse(JSON.stringify(config)) || {};
        Object.entries(result.resources)
    }
    catch(e){
        console.warn(`Failed to parse config ${lsc_str}`)
        localStorage.setItem("raconf", JSON.stringify(config))
    }

    if(!result.resources){
        result.resources = {}
    }
    const resources = result.resources

    for(let [resource_name, resource] of Object.entries(resources||{})){
        
        // link relationship to FK column
        if(!(resource.columns instanceof Array || resource.relationships instanceof Array)){
            continue
        }

        if(!resource.type){
            resource.type = resource_name
        }

        resource.search_cols = []
        result.resources[resource_name].name = resource_name
        let attributes = resource.columns || []

        for(let attr of attributes){
            for(let rel of resource.relationships || []){
                for(let fk of rel.fks || []){
                    if(attr.name == fk){
                        attr.relationship = rel;
                        attr.relationship.target_resource = result.resources[attr.relationship.target]
                    }
                }
            }
            if(attr.search){
                resource.search_cols.push(attr);
            }
        }
        resource.attributes = resource.columns
    }
    
    return result || reset_Conf()
}

export const reset_Conf = (reload) => {
    console.log("Resetting conf", config)
    localStorage.setItem("raconf", JSON.stringify(config));
    if(reload){
        window.location.reload()
    }
    return config
}

export const conf = get_Conf()

export default conf