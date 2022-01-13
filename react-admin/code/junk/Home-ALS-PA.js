import * as React from 'react';
import { styled } from '@mui/material/styles';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';

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
      <Accordion expanded={expanded === 'panel1'} onChange={handleChange('panel1')}>
        <AccordionSummary aria-controls="panel1d-content" id="panel1d-header">
          <Typography>Collapsible Group Item #1</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
            malesuada lacus ex, sit amet blandit leo lobortis eget. Lorem ipsum dolor
            sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
            sit amet blandit leo lobortis eget.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <div class="MuiTypography-root jss4">
      <div style="text-align:center">
        <Typography variant="h2">Welcome to API Logic Server - PA</Typography>
      </div>
      <h3><a class="custom" style="color: #3f51b5;"  rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/blob/main/README.md/" target="_blank">API Logic Server</a>
      creates <i>customizable</i> systems, instantly from your
      <a class="custom" style="color: #3f51b5;"  rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki/Sample-Database" target="_blank">database:</a>
      </h3>
      <h4>1. Automatic Admin App</h4>
      <ul>
         <li>For instant collaboration and Back Office data maintenance</li>
         <li>Rich functionality: multi-page, multi-table</li>
         <li><a class="custom" style="color: #3f51b5;"  rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki/Admin-Tour/" target="_blank">Explore</a> this Admin App,
              and how to <a class="custom" style="color: #3f51b5" rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App" target="_blank">customize it</a></li>
      </ul>
      <h4>2. API, with <a class="custom" style="color: #3f51b5;"  rel="nofollow" href="/api" target="_blank">oas/Swagger</a></h4>
      <ul>
         <li>For custom app dev, integration</li>
         <li>Rich functionality: endpoint for each table, with filtering, pagination, related data</li>
         <li><a class="custom" style="color: #3f51b5" rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki#customize-the-api-with-expose_servicespy-add-rpcs-services" target="_blank">Customizable</a>: add your own endpoints</li>
      </ul>
      <h4>3. Business Logic, for <span class="JoinedField" title="Often nearly half the app -- automation required"><span>backend processing</span> </span></h4>
      <ul>
         <li>Spreadsheet-like rules for multi-table derivations and constraints</li>
         <li>Extensible with Python events for email, messages, etc</li>
         <li><a class="custom" style="color: #3f51b5" rel="nofollow" href="https://github.com/valhuber/ApiLogicServer/wiki/Logic:-Rules-plus-Python" target="_blank">Explore</a>
             how logic can meaningfully improve
             <a class="custom" style="color: #3f51b5" rel="nofollow" href="https://github.com/valhuber/LogicBank/wiki/by-code" title="Rules are 40X more concise than code, and address over 95% of database logic" target="_blank">conciseness</a>
             and quality</li>
      </ul>

      </div>
    </div>
  );
}