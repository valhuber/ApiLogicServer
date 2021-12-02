import config from './Config.json'

const init_Conf = () => {
    if(! "raconf" in localStorage){
        console.log("Init Configuration")
        localStorage.setItem("raconf",JSON.stringify(config))
        window.location.reload()
    }
}

// als changes applied to config.js on 12/1
function loadResponse(url) {
    // see https://stackoverflow.com/questions/36921947/read-a-server-side-file-using-javascript
    // revise to https://developer.mozilla.org/en-US/docs/Web/API/Response
    // ala https://stackoverflow.com/questions/41946457/getting-text-from-fetch-response-object
    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url, false);
    try {
        xmlhttp.send()
    } catch (e) {
        console.warn(`Failed to send loadResponse ${e.toString()}`)
    }
    if (xmlhttp.status === 200) {
        result = xmlhttp.responseText;
    }
    return result;
}

export const get_Conf = () => {
    const yaml = require('js-yaml')
    init_Conf();

    let result = {}
    let ls_conf = null
    let yaml_str = ''
    yaml_str = loadResponse('http://localhost:5656/ui/admin/admin.yaml')  // for debug
    // yaml_str = loadResponse('/ui/admin/admin.yaml')                      // for release

    if (typeof yaml_str !== 'undefined' && yaml_str !== null) {
        console.log("Using als config via loadResponse")
        ls_conf = yaml.load( yaml_str );
        // ls_conf = JSON.parse(lsc_str)
        result = ls_conf // ? ls_conf : JSON.parse(JSON.stringify(config)) || {};
        Object.entries(result.resources)
    } else {
        console.log("Loading config from localStorage[raconf]")
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
    }

    if(!result.resources){
        result.resources = {}
    }
    const resources = result.resources

    for(let [resource_name, resource] of Object.entries(resources||{})){
        
        // link relationship to FK column
        if(!(resource.attributes instanceof Array || resource.relationships instanceof Array)){
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
        // resource.attributes = resource.columns
        // resource.columns = resource.attributes
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