import React from 'react';
import Paper from '@material-ui/core/Paper';
import {
  GroupingState,
  IntegratedGrouping,
} from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow,
  TableGroupRow,
  GroupingPanel,
  DragDropProvider,
  Toolbar, } from '@devexpress/dx-react-grid-material-ui';


function App() {

  //  useEffect(()=> {
  //   fetch('http://127.0.0.1:5000/', {
  //   'methods': 'GET',})
  //   .then(response => response.json().then(data => {setGetMessage(data);
  //   })
  //   );

  //  },[])

const columns = [
  { name: 'AssistanceProgramName', title: 'Assistance Program name' },
  { name: 'Eligibletreatments', title: 'Eligible treatments' },
  { name: 'Status', title: 'Status' },
  { name: 'GrantAmount', title: 'Grant Amount' },
];
const rows = [
  { AssistanceProgramName: 'AcuteMyeloidLeukemia', Eligibletreatments: 'Dexpak', Status: 'close',
GrantAmount: '$10,000' },
{ AssistanceProgramName: 'AcuteMyeloidLeukemia', Eligibletreatments: 'Dexpak', Status: 'close',
GrantAmount: '$30,000' },
];


return (
  <Paper>
    <Grid
      rows={rows}
      columns={columns}
    >
        <DragDropProvider />
        <GroupingState />
        <IntegratedGrouping />
        <Table />
        <TableHeaderRow />
        <TableGroupRow />
        <Toolbar />
        <GroupingPanel />
    </Grid>
  </Paper>
);
}

export default App;
