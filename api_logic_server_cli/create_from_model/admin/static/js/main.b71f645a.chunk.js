(this["webpackJsonpreact-apilogicserver"]=this["webpackJsonpreact-apilogicserver"]||[]).push([[3],{309:function(e){e.exports=JSON.parse('{"api_root":"http://localhost:5656/api","resources":{"Category":{"type":"Category","columns":[{"name":"Id","hidden":true},{"name":"CategoryName","label":"Custom Column Name","component":"SampleColumnField","search":true},{"name":"Description","style":{"font-weight":"bold","color":"blue"}}],"relationships":[],"label":"null"},"Customer":{"type":"Customer","user_component":"CustomerLabel","columns":[{"name":"Id"},{"name":"CompanyName"},{"name":"ContactName","search":true},{"name":"ContactTitle","search":true},{"name":"Address"},{"name":"City"},{"name":"Region"},{"name":"PostalCode"},{"name":"Country"},{"name":"Phone"},{"name":"Fax"},{"name":"Balance"},{"name":"CreditLimit"},{"name":"OrderCount"},{"name":"UnpaidOrderCount"}],"relationships":[{"name":"CustomerCustomerDemoList","target":"CustomerCustomerDemo","fks":["CustomerTypeId"],"direction":"tomany"},{"name":"OrderList","target":"Order","fks":["CustomerId"],"direction":"tomany"}],"label":null},"CustomerDemographic":{"type":"CustomerDemographic","columns":[{"name":"Id"},{"name":"CustomerDesc"}],"relationships":[],"label":null},"Employee":{"type":"Employee","label":"emps","user_component":"EmployeeLabel","columns":[{"name":"Id"},{"name":"LastName","search":true},{"name":"FirstName","search":true},{"name":"Title"},{"name":"TitleOfCourtesy"},{"name":"BirthDate"},{"name":"HireDate"},{"name":"Address"},{"name":"City"},{"name":"Region"},{"name":"PostalCode"},{"name":"Country"},{"name":"HomePhone"},{"name":"Extension"},{"name":"Photo"},{"name":"Notes"},{"name":"ReportsTo"},{"name":"PhotoPath"},{"name":"IsCommissioned"},{"name":"Salary"}],"relationships":[{"name":"Manager","target":"Employee","fks":["ReportsTo"],"direction":"toone"},{"name":"Manages","target":"Employee","fks":["ReportsTo"],"direction":"tomany"},{"name":"EmployeeAuditList","target":"EmployeeAudit","fks":["EmployeeId"],"direction":"tomany"},{"name":"EmployeeTerritoryList","target":"EmployeeTerritory","fks":["EmployeeId"],"direction":"tomany"},{"name":"OrderList","target":"Order","fks":["EmployeeId"],"direction":"tomany"}]},"Product":{"type":"Product","user_key":"ProductName","columns":[{"name":"Id"},{"name":"ProductName","search":true},{"name":"SupplierId"},{"name":"CategoryId"},{"name":"QuantityPerUnit"},{"name":"UnitPrice"},{"name":"UnitsInStock"},{"name":"UnitsOnOrder"},{"name":"ReorderLevel"},{"name":"Discontinued"},{"name":"UnitsShipped"}],"relationships":[{"name":"OrderDetailList","target":"OrderDetail","fks":["ProductId"],"direction":"tomany"}],"label":null},"Region":{"type":"Region","columns":[{"name":"Id"},{"name":"RegionDescription"}],"relationships":[],"label":null},"Shipper":{"type":"Shipper","columns":[{"name":"Id"},{"name":"CompanyName"},{"name":"Phone"}],"relationships":[],"label":null},"Supplier":{"type":"Supplier","columns":[{"name":"Id"},{"name":"CompanyName","search":true},{"name":"ContactName","search":true},{"name":"ContactTitle","search":true},{"name":"Address"},{"name":"City"},{"name":"Region"},{"name":"PostalCode"},{"name":"Country"},{"name":"Phone"},{"name":"Fax"},{"name":"HomePage"}],"relationships":[],"label":null},"Territory":{"type":"Territory","columns":[{"name":"Id"},{"name":"TerritoryDescription"},{"name":"RegionId"}],"relationships":[{"name":"EmployeeTerritoryList","target":"EmployeeTerritory","fks":["TerritoryId"],"direction":"tomany"}],"label":null},"CustomerCustomerDemo":{"type":"CustomerCustomerDemo","columns":[{"name":"Id"},{"name":"CustomerTypeId"}],"relationships":[{"name":"Customer","target":"Customer","fks":["CustomerTypeId"],"direction":"toone"}],"label":null},"EmployeeAudit":{"type":"EmployeeAudit","columns":[{"name":"Id"},{"name":"Title","search":true},{"name":"Salary"},{"name":"LastName","search":true},{"name":"FirstName","search":true},{"name":"EmployeeId"},{"name":"CreatedOn"}],"relationships":[{"name":"Employee","target":"Employee","fks":["EmployeeId"],"direction":"toone"}],"label":null},"EmployeeTerritory":{"type":"EmployeeTerritory","columns":[{"name":"Id"},{"name":"EmployeeId"},{"name":"TerritoryId"}],"relationships":[{"name":"Employee","target":"Employee","fks":["EmployeeId"],"direction":"toone"},{"name":"Territory","target":"Territory","fks":["TerritoryId"],"direction":"toone"}],"label":null},"Order":{"type":"Order","columns":[{"name":"Id"},{"name":"CustomerId"},{"name":"EmployeeId"},{"name":"OrderDate"},{"name":"RequiredDate"},{"name":"ShippedDate"},{"name":"ShipVia"},{"name":"Freight"},{"name":"ShipName","search":true},{"name":"ShipAddress","search":true},{"name":"ShipCity","search":true},{"name":"ShipRegion"},{"name":"ShipPostalCode"},{"name":"ShipCountry"},{"name":"AmountTotal"}],"relationships":[{"name":"Customer","target":"Customer","fks":["CustomerId"],"direction":"toone"},{"name":"Employee","target":"Employee","fks":["EmployeeId"],"direction":"toone"},{"name":"OrderDetailList","target":"OrderDetail","fks":["OrderId"],"direction":"tomany"}],"label":null},"OrderDetail":{"type":"OrderDetail","columns":[{"name":"Id"},{"name":"OrderId"},{"name":"ProductId"},{"name":"UnitPrice"},{"name":"Quantity"},{"name":"Discount"},{"name":"Amount"},{"name":"ShippedDate"}],"relationships":[{"name":"Order","target":"Order","fks":["OrderId"],"direction":"toone"},{"name":"Product","target":"Product","fks":["ProductId"],"direction":"toone"}],"label":null}}}')},707:function(e,t,n){},893:function(e,t){},926:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),o=n(86),c=n.n(o),i=n(22),s=n(238),l=n(1055),u=n(1041),d=n(1059),m=n(130),p=n(589),j=n(264),b=n(590),f=n(1),h=n(6),O=n(7),g=n(200),y=n(397),v=(Error,function(e){Object(h.a)(n,e);var t=Object(O.a)(n);function n(e,a,r){var o;return Object(f.a)(this,n),(o=t.call(this,e,a,r)).name="SafrsHttpError",o}return n}(y.a)),x={total:"total",headers:{Accept:"application/vnd.api+json; charset=utf-8","Content-Type":"application/vnd.api+json; charset=utf-8"},updateMethod:"PATCH",arrayFormat:"brackets",includeRelations:[],errorHandler:function(e){var t=e.body;return(null===t||void 0===t?void 0:t.errors.length)>0?new v(t.errors[0].title,e.status,t.errors[0].code):(console.log("Unsopported Http Error Body",e.body),e)},endpointToTypeStripLastLetters:["Model","s"]},C=n(8),S=n(24),k=n(2),I=function(){function e(t){if(Object(f.a)(this,e),this.lookup=void 0,this.includes=void 0,this.lookup=new Map,this.includes=[],"object"===typeof t){var n;n=Object.prototype.hasOwnProperty.call(t,"included")?[].concat(Object(S.a)(t.data),Object(S.a)(t.included)):t.data;var a,r=Object(C.a)(n);try{for(r.s();!(a=r.n()).done;){var o=a.value,c=this.getKey(o);this.lookup.set(c,o)}}catch(i){r.e(i)}finally{r.f()}}}return Object(k.a)(e,[{key:"getKey",value:function(e){return"".concat(e.type,":").concat(e.id)}},{key:"get",value:function(e){return this.has(e)?this.lookup.get(this.getKey(e)):e}},{key:"has",value:function(e){return this.lookup.has(this.getKey(e))}},{key:"unwrapData",value:function(e,t){var n=Object.assign({id:e.id,ja_type:e.type},e.attributes);return 0===t.length||Object.prototype.hasOwnProperty.call(e,"relationships")&&(n.relationships=e.relationships),n}}]),e}();var w=n(309);var E=function(){var e=n(523);"raconf"in localStorage||(console.log("Init Configuration"),localStorage.setItem("raconf",JSON.stringify(w)),window.location.reload());var t={},a={},r="";if(r=function(e){var t=null,n=new XMLHttpRequest;return n.open("GET",e,!1),n.send(),200===n.status&&(t=n.responseText),t}("http://localhost:5656/ui/admin/admin.yaml"),null!==r)r=(r=r.replace("<pre>","")).replace("</pre>",""),a=e.load(r),Object.entries(a.resources),delete a.info,delete a.about,delete a.properties_ref,delete a.settings,t=a.resources;else{null;var o=localStorage.getItem("raconf");try{a=JSON.parse(o)||(JSON.parse(JSON.stringify(w))||{}),Object.entries(a.resources)}catch(D){console.warn("Failed to parse config ".concat(o)),localStorage.setItem("raconf",JSON.stringify(w))}a.resources||(a.resources={}),t=a.resources}for(var c=0,s=Object.entries(t||{});c<s.length;c++){var l=Object(i.a)(s[c],2),u=l[0],d=l[1];if(d.hasOwnProperty("attributes")){d.columns=[],d.relationships=[],d.search_cols=[];var m,p=Object(C.a)(d.attributes);try{for(p.s();!(m=p.n()).done;){var j=m.value;if("string"==typeof j){var b={};b.name=j,d.columns.push(b)}else console.log("ignoring ".concat(j," in config"))}}catch(R){p.e(R)}finally{p.f()}for(var f=0,h=Object.entries(d.tab_groups||{});f<h.length;f++){var O=Object(i.a)(h[f],2),g=O[0],y=O[1],v={};v.name=g,v.fks=y.fks,v.target=y.resource,v.direction=y.direction,d.relationships.push(v)}delete d.attributes,delete d.tab_groups}if(d.columns instanceof Array||d.relationships instanceof Array){d.type||(d.type=u),d.search_cols=[],a.resources[u].name=u;var x,S=Object(C.a)(d.columns);try{for(S.s();!(x=S.n()).done;){var k,I=x.value,E=Object(C.a)(d.relationships||[]);try{for(E.s();!(k=E.n()).done;){var T,N=k.value,_=Object(C.a)(N.fks||[]);try{for(_.s();!(T=_.n()).done;){var L=T.value;I.name===L&&(I.relationship=N,I.relationship.target_resource=a.resources[I.relationship.target])}}catch(R){_.e(R)}finally{_.f()}}}catch(R){E.e(R)}finally{E.f()}I.search&&d.search_cols.push(I)}}catch(R){S.e(R)}finally{S.f()}console.log("".concat(u," search cols"),d.search_cols)}}a||P();return a||P()},P=function(e){return console.log("Resetting conf",w),localStorage.setItem("raconf",JSON.stringify(w)),e&&window.location.reload(),w},T=(E(),E());var N=n(637),_=n.n(N),L=n(1022),D=n(1028),R=n(1053),J=n(1052),A=n(1038),H=n(1079),M=n(1075),F=n(1076),U=n(282),B=n(1060),W=n(1051),q=n(1064),G=n(1039),K=n(1080),V=n(1040),z=n(509),Q=n(1062),X=n(347),Y=n(937),Z=n(1029),$=n(240),ee=n.n($),te=n(621),ne=n.n(te),ae=n(622),re=n.n(ae),oe=n(498),ce=n(935),ie=n(1056),se=n(1066),le=n(25),ue={position:"absolute",top:"50%",left:"50%",transform:"translate(-50%, -50%)",width:"75%",bgcolor:"background.paper",border:"2px solid #000",boxShadow:24,p:4,textAlign:"left"};function de(e){var t=e.label,n=e.content,r=e.resource_name,o=a.useState(!1),c=Object(i.a)(o,2),s=c[0],l=c[1];return Object(le.jsxs)("div",{children:[Object(le.jsxs)("span",{onClick:function(e){l(!0),e.stopPropagation()},className:"JoinedField",title:r,children:[t," "]}),Object(le.jsx)(se.a,{open:s,onClose:function(e){e.stopPropagation(),l(!1)},"aria-labelledby":"modal-modal-title","aria-describedby":"modal-modal-description",children:Object(le.jsxs)(ie.a,{sx:ue,children:[Object(le.jsx)(X.a,{id:"modal-modal-title",variant:"h6",component:"h2",children:t}),Object(le.jsx)(X.a,{id:"modal-modal-description",sx:{mt:2},children:n})]})})]})}var me=n(1058),pe=n(1063),je=n(641),be=(n(707),n(237)),fe=E(),he=[Object(le.jsx)(F.a,{source:"q",label:"Search",alwaysOn:!0})],Oe=function(e){var t=e.column,a=t.component,r=t.style||{},o=Object(le.jsx)(L.a,{source:t.name,style:r},t.name);if(!a)return o;try{var c=Object(oe.a)((function(){return n.e(0).then(n.bind(null,1088))}),{resolveComponent:function(e){return e[a]}});return Object(le.jsx)(c,{column:t})}catch(i){alert("Custom component error"),console.error("Custom component error",i)}return o},ge=function(e){var t,a,r=e.column,o=e.join,c=Object(U.b)();c.attributes&&Object.assign(c,c.attributes);var i=o.name,l=(c.id,o.target),u=(Object(s.a)(),o.fks[0]),d=null===(t=fe.resources[o.target])||void 0===t?void 0:t.user_key,m=Object(be.a)({type:"getOne",resource:l,payload:{id:c[u]}}),p=m.data,j=(m.loading,m.error,p||c[i]),b=null===(a=fe.resources[o.target])||void 0===a?void 0:a.user_component,f=null===j||void 0===j?void 0:j.id;if(j&&b)f=function(e,t){try{var a=Object(oe.a)((function(){return n.e(0).then(n.bind(null,1088))}),{resolveComponent:function(t){return t["".concat(e)]}});return Object(le.jsx)(a,{instance:t})}catch(r){alert("Custom component error"),console.error("Custom component error",r)}return null}(b,j);else if((null===j||void 0===j?void 0:j.attributes)&&d){r.relationship.target_resource.columns.filter((function(e){return e.name==d}));f=Object(le.jsx)("span",{children:j.attributes[d]||j.id})}var h=Object(le.jsx)(we,{instance:j,resource_name:o.target});return Object(le.jsx)(de,{label:f,content:h,resource_name:o.target},r.name)},ye=function(e,t){if(!t)return[];var n=t.filter((function(e){return"toone"===e.direction}));return e.map((function(e){if(e.hidden)return null;var t,a=Object(C.a)(n);try{for(a.s();!(t=a.n()).done;){var r,o=t.value,c=Object(C.a)(o.fks);try{for(c.s();!(r=c.n()).done;){var i=r.value;if(e.name==i)return Object(le.jsx)(ge,{column:e,join:o,label:e.label?e.label:e.name},e.name)}}catch(s){c.e(s)}finally{c.f()}}}catch(s){a.e(s)}finally{a.f()}return Object(le.jsx)(Oe,{column:e,label:e.label?e.label:e.name,style:e.header_style},e.name)}))},ve=function(e){return Object(le.jsx)(je.a,Object(m.a)({rowsPerPageOptions:[10,20,50,100],perPage:e.perPage||25},e))},xe=function(e,t,n,a){console.log("Delete",n),e.delete(t,n).then((function(){a()})).catch((function(e){return alert("error")}))},Ce=function(e){var t,n=e.column;e.resource;if("toone"==(null===(t=n.relationship)||void 0===t?void 0:t.direction)&&n.relationship.target){var a=fe.resources[n.relationship.target].search_cols,r=Object(le.jsx)(me.a,{optionText:""},n.name);return a?0==a.length?console.warn("no searchable columns configured for ".concat(n.relationship.target)):r=Object(le.jsx)(me.a,{optionText:a[0].name},n.name):console.error("no searchable columns configured"),Object(le.jsx)(pe.a,{source:n.name,label:"".concat(n.relationship.name," (").concat(n.name,")"),reference:n.relationship.target,children:r})}return Object(le.jsx)(F.a,{source:n.name})},Se=function(e){var t=e.record;return Object(le.jsx)("span",{children:t?"".concat(t.type?t.type+" ":""," #").concat(t.id," "):""})},ke=function(e){var t=e.source,n=Object(U.b)();return n?Object(le.jsx)(Ie,{label:t,value:n[t]}):null},Ie=function(e){var t=e.label,n=e.value;return Object(le.jsxs)(A.a,{item:!0,xs:3,children:[Object(le.jsx)(X.a,{variant:"body2",color:"textSecondary",component:"p",children:t}),Object(le.jsx)(X.a,{variant:"body2",component:"p",children:n})]})},we=function(e){var t=e.instance;if(!t||!t.type in fe.resources)return Object(le.jsx)("span",{});var n=t.type,a=fe.resources[n],r=(null===a||void 0===a?void 0:a.columns)||[];return Object(le.jsxs)("div",{style:{left:"-16px",position:"relative"},children:[Object(le.jsxs)("div",{style:{textAlign:"right",width:"100%"},children:[Object(le.jsxs)(ce.a,{title:"edit",component:G.a,to:{pathname:"".concat(n,"/").concat(t.id)},label:"Link",children:[Object(le.jsx)(ne.a,{}),"Edit"]}),Object(le.jsxs)(ce.a,{title:"view",component:G.a,to:{pathname:"/".concat(n,"/").concat(t.id,"/show")},label:"Link",children:[Object(le.jsx)(re.a,{}),"View"]})]}),Object(le.jsx)(A.a,{container:!0,children:r.map((function(e){return Object(le.jsx)(Ie,{label:e.name,value:t.attributes[e.name]},e.name)}))})]})},Ee=function(e){var t=e.columns,n=e.relationships,r=e.resource_name,o=e.id,c=Object(le.jsxs)(X.a,{variant:"h5",component:"h5",style:{margin:"30px 0px 30px"},children:["Instance Data ",Object(le.jsxs)("i",{style:{color:"#ccc"},children:[r,"  #",o]})]});return Object(le.jsxs)(V.a,{children:[c,Object(le.jsx)(A.a,{container:!0,spacing:3,margin:5,m:40,children:t.map((function(e){return Object(le.jsx)(ke,{source:e.name})}))}),Object(le.jsx)("hr",{style:{margin:"30px 0px 30px"}}),Object(le.jsx)(X.a,{variant:"h5",component:"h5",style:{margin:"30px 0px 30px"},children:n.length?"Related Data":""}),Object(le.jsx)(M.a,{tabs:Object(le.jsx)(z.a,{variant:"scrollable",scrollButtons:"auto"}),children:n.map((function(e){return"tomany"===e.direction?function(e,t,n){var r=Object(a.useState)(!0),o=Object(i.a)(r,2),c=(o[0],o[1]),l=Object(a.useState)(),u=Object(i.a)(l,2),d=(u[0],u[1]),m=Object(a.useState)(!1),p=Object(i.a)(m,2),j=(p[0],p[1]),b=Object(s.a)();Object(a.useEffect)((function(){b.getOne(e,{id:t}).then((function(e){var t=e.data;j(t.relationships),c(!1)})).catch((function(e){d(e),c(!1)}))}),[]);var f=fe.resources[n.target];if(!f)return console.warn("".concat(e,": No resource conf for ").concat(f)),Object(le.jsx)("span",{});if(!(null===f||void 0===f?void 0:f.columns))return console.log("No target resource columns"),Object(le.jsx)("div",{});var h=f.columns.filter((function(t){var n;return(null===(n=t.relationship)||void 0===n?void 0:n.target)!==e})),O=null===f||void 0===f?void 0:f.relationships,g=ye(h,O);return n.source=e,Object(le.jsx)(H.a,{label:n.name,children:Object(le.jsx)(R.a,{pagination:Object(le.jsx)(ve,{perPage:f.perPage}),children:Object(le.jsx)(K.a,{reference:n.target,target:n,addLabel:!1,children:Object(le.jsxs)(J.a,{rowClick:"show",children:[g,Object(le.jsx)(D.a,{})]})})})})}(r,o,e):function(e,t,n){var r=Object(a.useState)(!0),o=Object(i.a)(r,2),c=(o[0],o[1]),l=Object(a.useState)(),u=Object(i.a)(l,2),d=(u[0],u[1]),m=Object(a.useState)(!1),p=Object(i.a)(m,2),j=p[0],b=p[1],f=Object(s.a)();return Object(a.useEffect)((function(){f.getOne(e,{id:t}).then((function(e){var t,a,r=e.data;return{rel_resource:null===(t=r[n.target])||void 0===t?void 0:t.data.type,rel_id:null===(a=r[n.target])||void 0===a?void 0:a.data.id}})).then((function(e){var t=e.rel_resource,n=e.rel_id;console.log(t,n),f.getOne(t,{id:n}).then((function(e){var t=e.data;return b(t)})),c(!1)})).catch((function(e){d(e),c(!1)}))}),[]),Object(le.jsx)(H.a,{label:n.name,children:Object(le.jsx)(we,{instance:j})})}(r,o,e)}))})]})},Pe=function(e){window.addEventListener("storage",(function(){return window.location.reload()}));var t=r.a.useState(),n=(Object(i.a)(t,2)[1],Object(a.useState)(fe.resources[e.name])),o=Object(i.a)(n,2),c=o[0],l=(o[1],Object(a.useMemo)((function(){return e=c,function(t){var n=e.columns,a=e.relationships,r=ye(n,a),o=Object(s.a)(),c=Object(Y.a)(),i=[!1!==e.edit?Object(le.jsx)(D.a,{label:""},e.name):null,!1!==e.delete?Object(le.jsx)(Z.a,{onClick:function(e){e.stopPropagation()},render:function(e){return Object(le.jsx)(ee.a,{style:{fill:"#3f51b5"},onClick:function(n){return xe(o,t.resource,e,c)}})}},e.name):null];return Object(le.jsx)(R.a,Object(m.a)(Object(m.a)({filters:he,pagination:Object(le.jsx)(ve,{perPage:e.perPage})},t),{},{children:Object(le.jsxs)(J.a,{rowClick:"show",children:[r,i]})}))};var e}),[c])),d=Object(a.useMemo)((function(){return e=c,function(t){return Object(le.jsx)(q.a,Object(m.a)(Object(m.a)({},t),{},{children:Object(le.jsx)(W.a,{children:e.columns.map((function(t){return Object(le.jsx)(Ce,{column:t,resource:e},t.name)}))})}))};var e}),[c]),p=Object(a.useMemo)((function(){return function(e){var t=e.columns;return function(e){return Object(le.jsx)(B.a,Object(m.a)(Object(m.a)({},e),{},{children:Object(le.jsx)(W.a,{children:t.map((function(e){return Object(le.jsx)(Ce,{column:e},e.name)}))})}))}}(c)}),[c]),j=Object(a.useMemo)((function(){return function(e){return function(t){var n=e.columns,a=e.relationships;return Object(le.jsx)(Q.a,Object(m.a)(Object(m.a)({title:Object(le.jsx)(Se,{})},t),{},{children:Object(le.jsx)(Ee,{columns:n,relationships:a,resource_name:t.resource,id:t.id})}))}}(c)}),[c]);return Object(le.jsx)(u.a,Object(m.a)(Object(m.a)({},e),{},{list:l,edit:p,create:d,show:j}),e.name)},Te=n(1035),Ne=n(936),_e=n(211),Le=function(){return Object(le.jsxs)(Te.a,{children:[Object(le.jsx)(_e.b,{title:"Home"}),Object(le.jsxs)(Ne.a,{children:[Object(le.jsx)("h2",{children:"Welcome to API Logic Server"}),"Find \xa0",Object(le.jsx)("a",{class:"custom",rel:"nofollow",href:"http://localhost:5656/api",target:"_blank",children:"swagger here"}),", and \xa0",Object(le.jsx)("a",{class:"custom",rel:"nofollow",href:"https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App/",target:"_blank",children:"docs here"})]})]})},De=n(929),Re=n(1065),Je=n(311),Ae=n(1048),He=n(639),Me=n(1072),Fe=n(1070),Ue=n(1057),Be=n(1069),We=n(1050),qe=n(523),Ge=Object(Je.a)((function(e){return{widget:{border:"1px solid #3f51b5",marginRight:"1em",marginTop:"1em",marginBottom:"1em"},textInput:{width:"80%"}}})),Ke=function(){var e=[];try{e=JSON.parse(localStorage.getItem("raconfigs","{}"))}catch(c){}var t=a.useState(e&&e[0]),n=Object(i.a)(t,2),r=n[0],o=n[1];return Object(le.jsx)(Me.a,{sx:{minWidth:120},children:Object(le.jsxs)(Be.a,{fullWidth:!0,children:[Object(le.jsx)(Fe.a,{id:"demo-simple-select-label",children:"Config"}),Object(le.jsx)(We.a,{labelId:"demo-simple-select-label",id:"demo-simple-select",value:r,label:"Configs",size:"small",onChange:function(e){o(e.target.value)},defaultValue:"30",children:e?Object.entries(e).map((function(e){return Object(le.jsx)(Ue.a,{value:"30",children:"Ten"})})):null})]})})},Ve=function(){var e,t=Ge(),n=function(e){try{if(e){var t=JSON.parse(e);y(t.api_root)}p("#ddeedd"),localStorage.setItem("raconf",e),s||window.location.reload()}catch(n){p("red")}l(e)},r=localStorage.getItem("raconf")||JSON.stringify(P()),o=Object(a.useState)(r?JSON.stringify(JSON.parse(r),null,4):""),c=Object(i.a)(o,2),s=c[0],l=c[1],u=Object(a.useState)("black"),d=Object(i.a)(u,2),m=d[0],p=d[1],j=Object(a.useState)(!0),b=Object(i.a)(j,2),f=b[0],h=b[1],O=Object(a.useState)(null===(e=JSON.parse(r))||void 0===e?void 0:e.api_root),g=Object(i.a)(O,2),y=(g[0],g[1]);return Object(le.jsxs)("div",{children:[Object(le.jsxs)("div",{children:[Object(le.jsx)(Ke,{}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return n("")},color:"primary",children:"Clear"}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return n(JSON.stringify(P(),null,4))},color:"primary",children:"Reset"}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return window.location.reload()},color:"primary",children:"Apply"}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return localStorage.getItem("raconf"),void JSON.parse(localStorage.getItem("raconfigs","{}"))},color:"primary",children:"Save"}),Object(le.jsx)(Ae.a,{control:Object(le.jsx)(Re.a,{checked:f,onChange:function(e){h(e.target.checked)}}),label:"Auto Save Config"})]}),Object(le.jsx)("div",{children:Object(le.jsxs)(M.a,{children:[Object(le.jsx)(H.a,{label:"yaml",children:Object(le.jsx)(He.a,{language:"yaml",value:qe.dump(JSON.parse(s)),options:{theme:"vs-dark"},height:"1000px",style:{borderLeft:"8px solid ".concat(m)},onChange:function(e,t){return function(e,t){console.log(e);try{var a=qe.load(e);n(JSON.stringify(a)),p("black")}catch(r){console.warn("Failed to process",e),p("red")}}(e)}})}),Object(le.jsx)(H.a,{label:"json",children:Object(le.jsx)(De.a,{variant:"outlined",minRows:3,style:{width:"80%",backgroundColor:"white"},value:JSON.stringify(JSON.parse(s),null,4),onChange:function(e){return n(e.target.value)}})})]})})]})},ze=n(1054),Qe=n(51),Xe=n(299),Ye=n(626),Ze=n(443),$e=n(627),et=n(444),tt=n.n(et),nt=function(e){},at=function(e){var t=Object(Qe.f)(Xe.b);return Object(le.jsxs)(Ye.a,Object(m.a)(Object(m.a)({},e),{},{children:[t.map((function(e){return Object(le.jsx)(Ze.a,{to:"/".concat(e.name),primaryText:e.options&&e.options.label||e.name,leftIcon:e.icon?Object(le.jsx)(e.icon,{}):Object(le.jsx)(tt.a,{}),onClick:nt,sidebarIsOpen:true},e.name)})),Object(le.jsx)($e.a,{})]}))},rt=function(e){return Object(le.jsx)(ze.a,Object(m.a)(Object(m.a)({},e),{},{menu:at}))},ot=n(50),ct=n(14),it=n.n(ct),st=n(149),lt=n(253),ut=n(571),dt=n(451),mt=(n(138),n(344)),pt=n(310),jt=n(1061),bt=E();var ft=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,t=arguments.length>1?arguments[1]:void 0;t.type,t.payload;return e},ht=function(e){for(var t=0,n=Object.entries(bt.resources);t<n.length;t++){var a=Object(i.a)(n[t],2),r=a[0];if(a[1].type===e)return r}},Ot=function(e,t){var n,a,r,o,c=Object(mt.a)(e,t);if("CRUD_GET_ONE_SUCCESS"==t.type)return c;var s,l=Object(C.a)((null===(o=t.payload)||void 0===o?void 0:o.included)||[]);try{for(l.s();!(s=l.n()).done;){var u=s.value,d=ht(u.type);void 0!==u.type&&void 0!==u.id&&(c.resources[d][u.id]=u)}}catch(O){l.e(O)}finally{l.f()}if(Array.isArray(null===(n=t.payload)||void 0===n?void 0:n.data)){var m,p=Object(C.a)(t.payload.data);try{for(p.s();!(m=p.n()).done;){var j=m.value;if(j.relationships)for(var b=function(){var e,t,n=Object(i.a)(h[f],2),a=n[0],r=n[1],o=ht(null===(e=r.data)||void 0===e?void 0:e.type);o&&(Array.isArray(r.data)?j.relationships[a]=j[a]=r.data.map((function(e){return c.resources[o][e.id]})):(null===(t=r.data)||void 0===t?void 0:t.id)&&(j.relationships[a]=j[a]=c.resources[o][r.data.id]))},f=0,h=Object.entries(j.relationships);f<h.length;f++)b()}}catch(O){p.e(O)}finally{p.f()}}else null===(a=t.payload)||void 0===a||null===(r=a.data)||void 0===r||r.type;return c},gt=function(e){var t=e.authProvider,n=e.dataProvider,a=e.history,r=Object(st.b)({admin:Ot,router:Object(lt.b)(a),sReducer:ft}),o=it.a.mark((function e(){return it.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Object(ot.a)([Object(jt.a)(n,t)].map(ot.f));case 2:case"end":return e.stop()}}),e)})),c=Object(dt.a)(),i=st.c,s=Object(st.d)((function(e,t){return r(t.type!==pt.f?e:void 0,t)}),{},i(Object(st.a)(c,Object(ut.a)(a))));return c.run(o),s},yt=n(148),vt=n(638),xt=n.n(vt),Ct=Object(yt.b)(),St=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,t=arguments.length>1?arguments[1]:void 0,n=t.type,a=t.payload;return"RA/CRUD_GET_LIST_SUCCESS"===n&&(console.log("bcR",n,a),console.log(e)),e},kt=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{conf:{}},n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:j.a.fetchJson,a=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"Content-Range",r=Object(b.a)(x,t);t.conf;return{getList:function(t,a){var o,c=t;console.log("getList",t,a);var i=a.pagination,s=i.page,l=i.perPage,u={"page[number]":s,"page[size]":l,"page[offset]":(s-1)*l,"page[limit]":l,sort:" "};if((null===(o=a.filter)||void 0===o?void 0:o.q)&&"resources"in T){var d=T.resources[c].columns.filter((function(e){return 1==e.search})).map((function(e){return e.name}));console.log(d),u.filter=JSON.stringify(d.map((function(e){return{name:e,op:"like",val:"".concat(a.filter.q,"%")}}))),console.log(u.filter)}else Object.keys(a.filter||{}).forEach((function(e){u["filter[".concat(e,"]")]=a.filter[e]}));if(a.sort&&a.sort.field){var m="ASC"===a.sort.order?"":"-";u.sort="".concat(m).concat(a.sort.field)}var j=(T.resources[c].relationships||[]).map((function(e){return e.name}));u.include=j.join(",");var b="".concat(e,"/").concat(t,"?").concat(Object(p.stringify)(u));return n(b).then((function(e){var t=e.json,n=0;t.meta&&r.total&&(n=t.meta[r.total]),n=n||t.data.length;var a=new I(t),o=t.data.map((function(e){return a.unwrapData(e,j)}));return{data:o,included:t.included,total:n}})).catch((function(e){console.log("catch Error",e.body);var t=r.errorHandler;return Promise.reject(t(e))}))},getOne:function(t,a){var r="".concat(e,"/").concat(t,"/").concat(a.id,"?include=%2Ball");return n(r).then((function(e){var t=e.json.data,n=t.id,a=t.attributes,r=t.relationships,o=t.type;return Object.assign(a,r,{type:o},{relationships:r},{attributes:Object(m.a)({},a)}),{data:Object(m.a)({id:n},a)}}))},getMany:function(t,a){t=t;var o="filter[id]="+JSON.stringify(a.ids),c="".concat(e,"/").concat(t,"?").concat(o);return n(c).then((function(e){var t=e.json;console.log("gtMany",t);var n=0;return t.meta&&r.total&&(n=t.meta[r.total]),n=n||t.data.length,{data:t.data.map((function(e){return Object.assign({id:e.id,type:e.type},e.attributes)})),total:n}}))},getManyReference:function(t,r){var o,c;console.log("GMR"),console.log(t,r.target);var i=r.pagination,s=i.page,l=i.perPage,u=r.sort,d=u.field,p=u.order,j=(JSON.stringify([d,p]),JSON.stringify([(s-1)*l,s*l-1]),JSON.stringify(Object(m.a)({},r.filter)),null===(o=r.target)||void 0===o?void 0:o.name),b="".concat(e,"/").concat(null===(c=r.target)||void 0===c?void 0:c.source,"/").concat(r.id,"/").concat(j);return n(b,{}).then((function(e){var t,n=e.headers,r=e.json;return n.has(a)||console.debug("The ".concat(a," header is missing in the HTTP Response. The simple REST data provider expects responses for lists of resources to contain this header with the total number of results to build the pagination. If you are using CORS, did you declare ").concat(a," in the Access-Control-Expose-Headers header?")),{data:r.data,total:null===(t=r.data)||void 0===t?void 0:t.length}}))},update:function(t,a){var o=T.resources[t].type,c=r.endpointToTypeStripLastLetters;for(var i in c)if(t.endsWith(c[i])){o=t.slice(0,-1*c[i].length);break}var s={data:{id:a.id,type:o,attributes:a.data}};return n("".concat(e,"/").concat(t,"/").concat(a.id),{method:r.updateMethod,body:JSON.stringify(s)}).then((function(e){var t=e.json.data,n=t.id,a=t.attributes;return{data:Object(m.a)({id:n},a)}})).catch((function(e){console.log("catch Error",e.body);var t=r.errorHandler;return Promise.reject(t(e))}))},updateMany:function(t,a){return Promise.all(a.ids.map((function(r){return n("".concat(e,"/").concat(t,"/").concat(r),{method:"PUT",body:JSON.stringify(a.data)})}))).then((function(e){return{data:e.map((function(e){return e.json.id}))}}))},create:function(t,a){var o=t,c=r.endpointToTypeStripLastLetters;for(var i in c)if(t.endsWith(c[i])){o=t.slice(0,-1*c[i].length);break}var s={data:{type:o,attributes:a.data}};return n("".concat(e,"/").concat(t),{method:"POST",body:JSON.stringify(s)}).then((function(e){var t=e.json.data,n=t.id,a=t.attributes;return{data:Object(m.a)({id:n},a)}})).catch((function(e){console.log("catch Error",e.body);var t=r.errorHandler;return Promise.reject(t(e))}))},delete:function(t,a){return n("".concat(e,"/").concat(t,"/").concat(a.id),{method:"DELETE",headers:new Headers({"Content-Type":"text/plain"})}).then((function(e){return{data:e.json}}))},deleteMany:function(t,a){return Promise.all(a.ids.map((function(a){return n("".concat(e,"/").concat(t,"/").concat(a),{method:"DELETE",headers:new Headers({"Content-Type":"text/plain"})})}))).then((function(e){return{data:e.map((function(e){return e.json.id}))}}))},getResources:function(){return T?Promise.resolve({data:T}):n("".concat(e,"/schema"),{method:"GET"}).then((function(e){var t=e.json;return localStorage.setItem("raconf",JSON.stringify(t)),{data:t}})).catch((function(){return{data:{}}}))}}}(E().api_root,{}),It=function(){return Promise.resolve()},wt=function(){var e=Object(a.useState)(!1),t=Object(i.a)(e,2),n=t[0],r=t[1],o=Object(s.a)();return Object(a.useEffect)((function(){o.getResources().then((function(e){var t=Object.keys(e.data.resources).map((function(e){return{name:e}}));r(t)})).catch((function(e){console.warn(e),r([])}))}),[]),!1===n?Object(le.jsx)("div",{children:"Loading..."}):Object(le.jsx)(Qe.a,{store:gt({authProvider:It,dataProvider:o,history:Ct}),children:Object(le.jsxs)(l.a,{layout:rt,children:[Object(le.jsx)(u.a,{name:"Home",show:Le,list:Le,options:{label:"Home"},icon:_.a}),Object(le.jsx)(u.a,{name:"Configuration",show:Ve,list:Ve,options:{label:"Configuration"},icon:xt.a}),n.map((function(e){return Object(le.jsx)(Pe,{name:e.name},e.name)}))]})})},Et=function(){return Object(le.jsx)(d.a,{dataProvider:kt,customReducers:{admin2:St},children:Object(le.jsx)(wt,{})})},Pt=function(e){e&&e instanceof Function&&n.e(84).then(n.bind(null,1164)).then((function(t){var n=t.getCLS,a=t.getFID,r=t.getFCP,o=t.getLCP,c=t.getTTFB;n(e),a(e),r(e),o(e),c(e)}))};c.a.render(Object(le.jsx)(Et,{}),document.getElementById("root")),Pt()}},[[926,4,5]]]);
//# sourceMappingURL=main.b71f645a.chunk.js.map