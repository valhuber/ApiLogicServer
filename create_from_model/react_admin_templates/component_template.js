import {React} from 'react';
import { List, Datagrid, TextField, DateField, ReferenceField, NumberField, EditButton} from 'react-admin';
import {
    Edit,
    Show,
    SimpleForm,
    ReferenceInput,
    SelectInput,
    TextInput,
    DateInput,
    NumberInput,
    SimpleShowLayout,
    ReferenceManyField
} from 'react-admin';
import Grid from '@material-ui/core/Grid';

const customerFilters = [
    <TextInput source="q" label="Search" alwaysOn />
];


export const ApiLogicServer_componentList = props => (
    <List filters={customerFilters} perPage={10}  {...props} >
        <Datagrid rowClick="show">
            // ApiLogicServer_list_columns
            <EditButton />
        </Datagrid>
    </List>
);


export const ApiLogicServer_componentEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            // ApiLogicServer_edit_columns
        </SimpleForm>
    </Edit>
);


export const ApiLogicServer_componentAdd = props => (
    <Edit {...props}>
        <SimpleForm>
            // ApiLogicServer_add_columns
        </SimpleForm>
    </Edit>
);


const ApiLogicServer_componentTitle = ({ record }) => {
    return <span>Post {record ? `ID: "${record.id}" ContactName: "${record.ContactName}"` : ''}</span>;
};


export const CustomerShow = props => { 

    return (

    <Show title={<ApiLogicServer_componentTitle />} {...props}>
        <SimpleShowLayout>
            // ApiLogicServer_show_columns
            // ApiLogicServer_related
        </SimpleShowLayout>
    </Show>
    );
}