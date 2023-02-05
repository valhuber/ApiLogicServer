import * as React from 'react';
import { styled } from '@mui/material/styles';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import { typography } from '@material-ui/system';

const Accordion = styled((props) => (
  <MuiAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
  border: `1px solid ${theme.palette.divider}`,
  '&:not(:last-child)': {
    borderBottom: 0,
  },
  '&:before': {
    display: 'none',
  },
}));

const AccordionSummary = styled((props) => (
  <MuiAccordionSummary
    expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: '0.9rem' }} />}
    {...props}
  />
))(({ theme }) => ({
  backgroundColor:
    theme.palette.mode === 'dark'
      ? 'rgba(255, 255, 255, .05)'
      : 'rgba(0, 0, 0, .03)',
  flexDirection: 'row-reverse',
  '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
    transform: 'rotate(90deg)',
  },
  '& .MuiAccordionSummary-content': {
    marginLeft: theme.spacing(1),
  },
}));

const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
  padding: theme.spacing(2),
  borderTop: '1px solid rgba(0, 0, 0, .125)',
}));

export default function CustomizedAccordions() {
  const [expanded, setExpanded] = React.useState('panel1');
  const handleChange = (panel) => (event, newExpanded) => {
    setExpanded(newExpanded ? panel : false);
  };
  return (
    <div>
      <div className="MuiTypography-root jss4">
      <Typography variant="h4" align="center">Welcome to API Logic Server -- Sample System</Typography>
      <Typography lineHeight = {2}><br></br><a   rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/blob/main/README.md/" target="_blank">API Logic Server</a>
      &nbsp;creates <i>customizable</i> model-driven systems, instantly from your&nbsp;
      <a  href="https://apilogicserver.github.io/Docs/Sample-Database/" target="_blank">database</a>.
      <Typography><br></br></Typography>
      </Typography>
      <Accordion  >
        <AccordionSummary aria-controls="panel1d-content" id="panel1d-header">
          <Typography>This app was not coded - it was <i>created.</i> Click here to see how:</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
          <ul>
            <li><i>Automated: </i>create executable systems with this single command...
              <pre>
              &nbsp;&nbsp;&nbsp;ApiLogicServer <strong>create-and-run</strong> \<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--project_name=ApiLogicProject \  # customize with Python and your IDE<br></br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--db_url=sqlite:///nw.sqlite      # your db here
              </pre>
              </li>
            <li><i>Model-driven: </i>creation builds executable&nbsp;
            <a rel="nofollow" href="https://apilogicserver.github.io/Docshitecture/#customizable-declarative-models" target="_blank">models</a>
              , not code
                <ul>
                    <li>
                    Dramatically simpler to understand, customize and maintain
                    </li>
                </ul>
              <Typography>&nbsp;</Typography></li>
            <li><i>Customizable: </i>models are created into a project;&nbsp;
              <a rel="nofollow" href="https://apilogicserver.github.io/Docsject-Structure/" target="_blank">customize</a>
              &nbsp;with Python and your IDE
              <ul>
                  <li>This system has about 20 rules, and 20 lines of code</li>
              </ul>
            </li>
          </ul>
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Typography><br></br>
      1.&nbsp;
          <a href="https://apilogicserver.github.io/Docsin-Tour/" target="_blank">Automatic Admin App</a>
          , you are running it now
      <ul>
         <li>For instant collaboration and Back Office data maintenance</li>
         <li>Rich functionality: multi-page, multi-table, automatic joins</li>
         <li>Explore this app (e.g., click Customer, at left),
              and how to <a  rel="nofollow" href="https://apilogicserver.github.io/Docsin-Customization/" target="_blank">customize it</a></li>
      </ul>
      2. <a href="/api" target="_blank">API</a>, with oas/Swagger
      <ul>
         <li>For custom app dev, application integration</li>
         <li>Rich functionality: endpoint for each table, with filtering, pagination, related data</li>
         <li><a rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki#customize-the-api-with-expose_servicespy-add-rpcs-services" target="_blank">Customizable</a>: add your own endpoints</li>
      </ul>
      3.&nbsp;
      <a  rel="nofollow" href="https://apilogicserver.github.io/Docsic/" target="_blank">Business Logic</a>
          , for <span title="Often nearly half the app -- automation required"><span>backend processing</span> </span>
      <ul>
         <li>Spreadsheet-like rules for multi-table derivations and constraints</li>
         <li>Extensible with Python events for email, messages, etc</li>
         <li>Explore
             &nbsp;how logic can meaningfully improve&nbsp;
             <a  rel="nofollow" href="https://github.com/valhuber/LogicBank/wiki/by-code" title="Rules are 40X more concise than code, and address over 95% of database logic" target="_blank">conciseness</a>
             &nbsp;and quality</li>
      </ul>
      </Typography>

      </div>

    </div>
  );
}