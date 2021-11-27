import config from './Config.json'

const init_Conf = () => {
    if(! ("raconf" in localStorage)){
        console.log("Init Configuration")
        localStorage.setItem("raconf",JSON.stringify(config))
        window.location.reload()
    }
}

function handleErrors(response) {  // https://www.tjvantoll.com/2015/09/13/fetch-and-errors/
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
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

    for (let [resource_name, resource] of Object.entries(resources||{})) {
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

function loadFileUgh(filePath) {
    // see https://stackoverflow.com/questions/36921947/read-a-server-side-file-using-javascript
    // revise to https://developer.mozilla.org/en-US/docs/Web/API/Response
    // ala https://stackoverflow.com/questions/41946457/getting-text-from-fetch-response-object
    let use_promise = false
    if (use_promise) {
        fetch(filePath)
            .then(handleErrors)
            .then(
                function(response) {
                    return response.text().then(function(text) {
                        console.log('loadfile - fetach response working')
                        result = text;
                    });
            })
            .catch(
                err => console.log('loadfile - error detection [no server, url] ok (for non-ALS operation: ' + err));
        console.log('loadfile - fetch issued... now what?  Must rest of config.js be in callback??')
    } else {
        var result = null;
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", filePath, false);

        try {
            xmlhttp.send()
        } catch (e) {
            console.warn(`Failed to send loadFile ${e.toString()}`)
        }
        if (xmlhttp.status === 200) {
            result = xmlhttp.responseText;
        }
    }
    return result;
}

async function httpGetPromise(url) {
    // see https://stackoverflow.com/questions/36921947/read-a-server-side-file-using-javascript
    // revise to https://developer.mozilla.org/en-US/docs/Web/API/Response
    // ala https://stackoverflow.com/questions/41946457/getting-text-from-fetch-response-object
    // maybe https://exploringjs.com/es6/ch_promises.html#sec_creating-using-promises
    return new Promise(
        function (resolve, reject) {
            const request = new XMLHttpRequest();
            request.onload = function () {
                if (this.status === 200) {
                    // Success
                    console.log('httpGet - fetch response working')
                    return resolve(this.response);
                } else {
                    console.log('httpGet - error detection [no server, url] ok (for non-ALS operation: ' +
                        this.statusText)
                    reject(new Error(this.statusText));
                }
            };
            request.onerror = function () {
                reject(new Error(
                    'XMLHttpRequest Error: '+this.statusText));
            };
            request.open('GET', url);
            request.send();
        });
}

async function httpGetNestAwait(url) {
    // see https://stackoverflow.com/questions/36921947/read-a-server-side-file-using-javascript
    // revise to https://developer.mozilla.org/en-US/docs/Web/API/Response
    // ala https://stackoverflow.com/questions/41946457/getting-text-from-fetch-response-object
    // maybe https://exploringjs.com/es6/ch_promises.html#sec_creating-using-promises
    const request = new XMLHttpRequest();
    request.onload = async function () {
        if (this.status === 200) {
            // Success
            console.log('httpGet - fetch response working')
            return await Promise.resolve(this.response);
        } else {
            console.log('httpGet - error detection [no server, url] ok (for non-ALS operation: ' +
                this.statusText)
            Promise.reject(new Error(this.statusText));
        }
    };
    request.onerror = function () {
        Promise.reject(new Error(
            'XMLHttpRequest Error: '+this.statusText));
    };
    request.open('GET', url);
    request.send();
}

async function myFetch(url) {  // try to sync up with await
    // https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await
    let response = await fetch(url);
    if (!response.ok) {
        throw new Error(`myFetch - HTTP error! status: ${response.status}`);
    }
    return await response.text()
    // console.log('myFetch returning ' + theResult.substring(1,12))
    // return response.text()
}

export const get_Conf = () => {
    const yaml = require('js-yaml')
    init_Conf();
    let resources = {}
    let result = {}
    let yaml_str = ''
    let ls_conf = null
    console.log('get_Conf fetching...')
    let caller1 = false
    if (caller1) {
        myFetch('http://localhost:5656/ui/admin/admin.yaml')
            .then((text) => {
                yaml_str = text;
                console.log('get_Conf got yaml_str: " + yaml_str.substring(1,32)')
            })
            .catch(e => console.log('get_conf call to myFetch fails with: ' + e.message));
    } else {
        myFetch('http://localhost:5656/ui/admin/admin.yaml')
            .then(
                async function (value) {
                    yaml_str = value
                    console.log('get_conf got it: ' + value.substring(1, 32));
                    return process_yaml_or_use_import_local_storage(yaml_str)
                },
                function (reason) {
                    console.log('get_conf ailed with: ', reason, ', using import/localsorage');
                });
    }
    console.log('getConf - myFetch requested, proceeding')
    let is_sync = false
    if (is_sync) {

        if (typeof yaml_str !== 'undefined' && yaml_str !== null) {
            yaml_str = yaml_str.replace('<pre>', '')
            yaml_str = yaml_str.replace('</pre>', '')
            ls_conf = yaml.load(yaml_str);
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
            } catch (e) {
                console.warn(`Failed to parse config ${lsc_str}`)
                localStorage.setItem("raconf", JSON.stringify(config))
            }

            if (!result.resources) {
                result.resources = {}
            }
            resources = result.resources
        }

        for (let [resource_name, resource] of Object.entries(resources || {})) {
            if (resource.hasOwnProperty('attributes')) {  // convert attr format
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
                for (const [each_tab_name, each_tab_group] of Object.entries(resource.tab_groups || {})) {
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
            if (!(resource.columns instanceof Array || resource.relationships instanceof Array)) {
                continue
            }

            if (!resource.type) {
                resource.type = resource_name
            }

            resource.search_cols = []
            result.resources[resource_name].name = resource_name

            for (let col of resource.columns) {
                for (let rel of resource.relationships || []) {
                    for (let fk of rel.fks || []) {
                        if (col.name === fk) {
                            col.relationship = rel;
                            col.relationship.target_resource = result.resources[col.relationship.target]
                        }
                    }
                }
                if (col.search) {
                    resource.search_cols.push(col);
                }
            }
            console.log(`${resource_name} search cols`, resource.search_cols)
        }
        let returning = result || reset_Conf()
        // let returning_str = JSON.stringify(returning)
        return result || reset_Conf()
    }
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
