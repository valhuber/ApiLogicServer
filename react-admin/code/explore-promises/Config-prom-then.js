import config from './Config.json'

const init_Conf = () => {
    if(! ("raconf" in localStorage)){
        console.log("Init Configuration")
        localStorage.setItem("raconf",JSON.stringify(config))
        window.location.reload()
    }
}

export const get_Conf = () => {  // do it all from .then (still returns after issue)
    // returns object of
    // see https://stackoverflow.com/questions/36921947/read-a-server-side-file-using-javascript
    // revise to https://developer.mozilla.org/en-US/docs/Web/API/Response
    // ala https://stackoverflow.com/questions/41946457/getting-text-from-fetch-response-object
    const yaml = require('js-yaml')
    init_Conf();
    let resources = {}
    let result = {}
    let yaml_str = ''
    let ls_conf = null  // todo - parameters for host, port, path
    let filePath = 'http://localhost:5656/ui/admin/admin.yaml'
    let use_promise = true
    if (use_promise) {
        fetch(filePath)
            .then(
                function(response) {
                    if (!response.ok) {  // fall back to import, localstorage
                        console.log('get_Conf - bad response - fall back to import, localstorage: ');
                        return process_yaml_or_use_import_local_storage(null)
                    }
                })
            .then(
                function(response) {
                    return response.text().then(function(yaml_text) {
                        console.log('get_Conf - fetch response working')
                        return process_yaml_or_use_import_local_storage(yaml_text)
                    });
                })
            .catch(err => {
                console.log('get_Conf - exception - fall back to import, localstorage for non-ALS: ' + err);
                return process_yaml_or_use_import_local_storage(null)
            });
        console.log('loadfile - fetch issued... now what?  I guess the rest of config.js is in then.??')
    } else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", filePath, false);

        try {
            xmlhttp.send()
        } catch (e) {
            console.warn(`get_Conf - Failed to send XMLHttpRequest ${e.toString()}`)
            return process_yaml_or_use_import_local_storage(null)
        }
        if (xmlhttp.status === 200) {
            let yaml_text = xmlhttp.responseText;
            return process_yaml_or_use_import_local_storage(yaml_text)
        } else {
            console.warn(`get_Conf - bad XMLHttpRequest status ${xmlhttp.status}`)
            return process_yaml_or_use_import_local_storage(null)
        }
    }
}

const process_yaml_or_use_import_local_storage = (yaml_str) => {
    const yaml = require('js-yaml')
    init_Conf();
    let resources = {}
    let result = {}
    let ls_conf = null  // todo - parameters for host, port, path
    if (yaml_str !== null) {
      yaml_str = yaml_str.replace('<pre>','')
      yaml_str = yaml_str.replace('</pre>','')
      ls_conf = yaml.load( yaml_str );
      // ls_conf = JSON.parse(lsc_str)
      result = ls_conf // ? ls_conf : JSON.parse(JSON.stringify(config)) || {};
      Object.entries(result.resources)
      // delete result.info
      // delete result.about
      // delete result.properties_ref
      // delete result.settings
      resources = result.resources
    } else {
      ls_conf = null
      const lsc_str = localStorage.getItem("raconf")
      try {
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
      resources = result.resources
    }

    for(let [resource_name, resource] of Object.entries(resources||{})){
        if (resource.hasOwnProperty('attributes')) {  // convert attr -> col format
          // use npm start, launches browswer at http://localhost:3000/admin-app#/Home
          resource.columns = []
          resource.relationships = []
          resource.search_cols = []
          for (let each_attribute of resource.attributes) {
            if (typeof each_attribute == 'string') {
              let each_attribute_object = {}
              each_attribute_object.name = each_attribute
              resource.columns.push(each_attribute_object)
            } else {
              console.log(`ignoring ${each_attribute} in config`)
            }
          }
          for (const [each_tab_name, each_tab_group] of Object.entries(resource.tab_groups||{}) ) {
            let relationship_object = {}
            relationship_object.name = each_tab_name
            relationship_object.fks = each_tab_group.fks
            relationship_object.direction = each_tab_group.direction
            if (each_tab_group.direction === "toone") {
                relationship_object.target = each_tab_group.target
            } else if (each_tab_group.direction === "tomany") {
                relationship_object.target = each_tab_group.resource
            } else {
                relationship_object.target = each_tab_group.resource
            }
            resource.relationships.push(relationship_object)
          }
          // delete resource.attributes  // save some memory
          // delete resource.tab_groups
        }
        // link relationship to FK column
        if(!(resource.columns instanceof Array || resource.relationships instanceof Array)){
            continue
        }

        if(!resource.type){
            resource.type = resource_name
        }

        resource.search_cols = []
        result.resources[resource_name].name = resource_name

        for(let col of resource.columns){
            for(let rel of resource.relationships || []){
                for(let fk of rel.fks || []){
                    if(col.name === fk){
                        col.relationship = rel;
                        col.relationship.target_resource = result.resources[col.relationship.target]
                    }
                }
            }
            if(col.search){
                resource.search_cols.push(col);
            }
        }
        console.log(`${resource_name} search cols`, resource.search_cols)
    }
    let returning = result || reset_Conf()
    // let returning_str = JSON.stringify(returning) -- this fails with circular loops for non ALS
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
