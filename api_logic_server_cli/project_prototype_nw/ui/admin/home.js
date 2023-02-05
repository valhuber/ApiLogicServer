const sla_doc =
    '<div class="MuiTypography-root jss4" style="color: rgba(0, 0, 0, 0.66)">' +
    '<div style="text-align:center">' +
    '<h2>Welcome to API Logic Server - Sample</h2>' +
    '</div><br>' +
    '<h3><a class="custom" style="color: #3f51b5;"  rel="nofollow" href="https://apilogicserver.github.io/Docs/" target="_blank">API Logic Server</a> ' +
    'creates <i>customizable</i> model-driven systems, instantly from your ' +
    '<a class="custom" style="color: #3f51b5;"  rel="nofollow" href="https://apilogicserver.github.io/Docs/Sample-Database/" target="_blank">database:</a>' +
    '</h3>' +
    '<h4>1. Automatic Admin App</h4>' +
    '<ul>' +
    '   <li>For instant collaboration and Back Office data maintenance</li>' +
    '   <li>Rich functionality: multi-page, multi-table, automatic joins, declarative hide/show</li>' +
    '   <li><a class="custom" style="color: #3f51b5;"  rel="nofollow" href="https://apilogicserver.github.io/Docs/Admin-Tour/" target="_blank">Explore</a> this Admin App, ' +
    '        and how to <a class="custom" style="color: #3f51b5" rel="nofollow" href="https://apilogicserver.github.io/Docsin-Customization/" target="_blank">customize it</a></li>' +
    '</ul>' +
    '<h4>2. API, with <a class="custom" style="color: #3f51b5;"  rel="nofollow" href="/api" target="_blank">oas/Swagger</a></h4>' +
    '<ul>' +
    '   <li>For custom app dev, integration</li>' +
    '   <li>Rich functionality: endpoint for each table, with filtering, pagination, related data</li>' +
    '   <li><a class="custom" style="color: #3f51b5" rel="nofollow" href="https://apilogicserver.github.io/Docs/API-Customize/" target="_blank">Customizable</a>: add your own endpoints</li>' +
    '   <li><a class="custom" style="color: #3f51b5" rel="nofollow" href="http://localhost:5656/stop" target="_blank">Stop</a> the server</li>' +
    '</ul>' +
    '<h4>3. Business Logic, for <span class="JoinedField" title="Often nearly half the app -- automation required"><span>backend processing</span> </span></h4>' +
    '<ul>' +
    '   <li>Spreadsheet-like rules for multi-table derivations and constraints</li>' +
    '   <li>Extensible with Python events for email, messages, etc</li>' +
    '   <li><a class="custom" style="color: #3f51b5" rel="nofollow" href="https://apilogicserver.github.io/Docs/Logic/" target="_blank">Explore</a> ' +
    '       how logic can meaningfully improve ' +
    '       <a class="custom" style="color: #3f51b5" rel="nofollow" href="https://apilogicserver.github.io/Docs/Logic-Why/#rules-executable-design" title="Rules are 40X more concise than code, and address over 95% of database logic" target="_blank">conciseness</a> ' +
    '       and quality</li>' +
    '   <li><a class="custom" style="color: #3f51b5" rel="nofollow" href="https://apilogicserver.github.io/Docs/Logic-Tutorial/" target="_blank">Test</a> ' +
    '       using Behave, a TDD (Test Driven Design) framework </li>' +
    '</ul><br/><br/>' +
    '<h4>Explore this app</h4>' +
    '   <ul><li>Start with Customer (at left), and watch for the Info icons (upper right)</li></ul>' +
    '</div>'


function getContent(){

    let result = '<button class="MuiButtonBase-root MuiButton-root MuiButton-text makeStyles-widget-159 MuiButton-textPrimary" tabindex="0" type="button" ><span class="MuiButton-label">Loaded External Component. </span></button>';
    result = ""
    result += sla_doc;
    return result;
}

