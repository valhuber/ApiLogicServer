const sla_doc = '<div class="MuiTypography-root"><center><h1>Welcome to API Logic Server</h1></center><br>' +
    '<h2>Automatic Admin App, Designed For</h2>' +
    '<ul><li>Instant Business User Collaboration - Working Software <i>Now</i></li>' +
    '<li>Back Office Data Maintenance</li></ul>' +
    '<br><h2>Key Features</h2>' +
    '<ul>' +
    '<li><strong>Multi-page:</strong> screen transitions</li>' +
    '<li><strong>Multi-table:</strong> child grids, parent joins</li>' +
    '<li><strong>Logic aware:</strong> multi-table derivations and constraints, extensible with Python events for email, messages, etc</li>' +
    '<li><strong>Customizable:</strong> see ui/admin/admin.yaml.  Use SAFRS API for custom apps.</li></ul>' +
    '<br><h2>Resources</h2>' +
    '<ul>' +
    '<li><a class="custom" rel="nofollow" href="http://localhost:5656/api" target="_blank">Swagger</a></li>' +
    '<li><a class="custom" rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/blob/main/README.md/" target="_blank">API Logic Server Docs</a></li>' +
    '<li><a class="custom" rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App/" target="_blank">Admin App Customization Docs</a></li>' +
    '</ul>' +
    '</div>'


function getContent(){

    let result = '<button class="MuiButtonBase-root MuiButton-root MuiButton-text makeStyles-widget-159 MuiButton-textPrimary" tabindex="0" type="button" ><span class="MuiButton-label">Loaded External Component. </span></button>';
    result = ""
    result += sla_doc;
    return result;
}

