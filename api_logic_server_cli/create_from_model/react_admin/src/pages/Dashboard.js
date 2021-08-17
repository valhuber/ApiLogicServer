import React from 'react'
import { Card, CardContent, CardHeader } from '@material-ui/core'
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <Card>
      <CardHeader title="Welcome!"> 

      </CardHeader>
      <CardContent> Welcome to APILogicServer Web Dashboard</CardContent>
      <Button
            color="primary"
            component={Link}
            to={{
                pathname: '/Customer'
            }}
        >
            See all customers!
        </Button>
    </Card>
  )
}

export default Dashboard
