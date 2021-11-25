(this["webpackJsonpreact-apilogicserver"]=this["webpackJsonpreact-apilogicserver"]||[]).push([[3],{309:function(e){e.exports=JSON.parse('{"api_root":"//thomaxxl.pythonanywhere.com/api","resources":{"People":{"type":"Person","user_key":"name","columns":[{"name":"id","hidden":true},{"name":"name"},{"name":"email"},{"name":"comment"},{"name":"dob"},{"name":"employer_id"},{"name":"_password"}],"relationships":[{"name":"books_read","target":"Books","fks":["reader_id"],"direction":"tomany"},{"name":"books_written","target":"Books","fks":["author_id"],"direction":"tomany"},{"name":"reviews","target":"Reviews","fks":["reader_id"],"direction":"tomany"},{"name":"friends","target":"People","fks":["friend_a_id","friend_b_id"],"direction":"tomany"}],"label":null},"Books":{"type":"Book","user_key":"title","columns":[{"name":"id","hidden":true},{"name":"title"},{"name":"reader_id"},{"name":"author_id"},{"name":"publisher_id"},{"name":"published"}],"relationships":[{"name":"publisher","target":"Publishers","fks":["publisher_id"],"direction":"toone"},{"name":"reviews","target":"Reviews","fks":["book_id"],"direction":"tomany"},{"name":"reader","target":"People","fks":["reader_id"],"direction":"toone"},{"name":"author","target":"People","fks":["author_id"],"direction":"toone"}],"label":null},"Reviews":{"type":"Review","columns":[{"name":"book_id"},{"name":"reader_id"},{"name":"review"},{"name":"created"}],"relationships":[{"name":"book","target":"Books","fks":["book_id"],"direction":"toone"},{"name":"reader","target":"People","fks":["reader_id"],"direction":"toone"}],"label":null},"Publishers":{"type":"Publisher","columns":[{"name":"id"},{"name":"name"}],"relationships":[{"name":"books","target":"Books","fks":["publisher_id"],"direction":"tomany"}],"label":null}}}')},707:function(e,t,n){},893:function(e,t){},926:function(e,t,n){"use strict";n.r(t);var r=n(0),a=n.n(r),o=n(86),c=n.n(o),i=n(22),s=n(238),l=n(1055),u=n(1041),d=n(1059),j=n(130),b=n(498),f=n(264),h=n(590),p=n(1),O=n(6),m=n(7),v=n(200),g=n(397),y=(Error,function(e){Object(O.a)(n,e);var t=Object(m.a)(n);function n(e,r,a){var o;return Object(p.a)(this,n),(o=t.call(this,e,r,a)).name="SafrsHttpError",o}return n}(g.a)),x={total:"total",headers:{Accept:"application/vnd.api+json; charset=utf-8","Content-Type":"application/vnd.api+json; charset=utf-8"},updateMethod:"PATCH",arrayFormat:"brackets",includeRelations:[],errorHandler:function(e){var t=e.body;return(null===t||void 0===t?void 0:t.errors.length)>0?(alert("Error "+t.errors[0].title),new y(t.errors[0].title,e.status,t.errors[0].code)):(console.log("Unsopported Http Error Body",e.body),e)},endpointToTypeStripLastLetters:["Model","s"]},S=n(8),w=n(25),k=n(2),_=function(){function e(t){if(Object(p.a)(this,e),this.lookup=void 0,this.includes=void 0,this.lookup=new Map,this.includes=[],"object"===typeof t){var n;n=Object.prototype.hasOwnProperty.call(t,"included")?[].concat(Object(w.a)(t.data),Object(w.a)(t.included)):t.data;var r,a=Object(S.a)(n);try{for(a.s();!(r=a.n()).done;){var o=r.value,c=this.getKey(o);this.lookup.set(c,o)}}catch(i){a.e(i)}finally{a.f()}}}return Object(k.a)(e,[{key:"getKey",value:function(e){return"".concat(e.type,":").concat(e.id)}},{key:"get",value:function(e){return this.has(e)?this.lookup.get(this.getKey(e)):e}},{key:"has",value:function(e){return this.lookup.has(this.getKey(e))}},{key:"unwrapData",value:function(e,t){var n=Object.assign({id:e.id,ja_type:e.type},e.attributes);return 0===t.length||Object.prototype.hasOwnProperty.call(e,"relationships")&&(n.relationships=e.relationships),n}}]),e}();var C=n(309);var P=function(){var e=n(524);"raconf"in localStorage||(console.log("Init Configuration"),localStorage.setItem("raconf",JSON.stringify(C)),window.location.reload());var t={},r={},a="";if(a=function(e){var t=null,n=new XMLHttpRequest;n.open("GET",e,!1);try{n.send()}catch(r){console.warn("Failed to send loadFile ".concat(r.toString()))}return 200===n.status&&(t=n.responseText),t}("http://localhost:5656/ui/admin/admin.yaml"),"undefined"!==typeof a&&null!==a)a=(a=a.replace("<pre>","")).replace("</pre>",""),r=e.load(a),Object.entries(r.resources),t=r.resources;else{null;var o=localStorage.getItem("raconf");try{r=JSON.parse(o)||(JSON.parse(JSON.stringify(C))||{}),Object.entries(r.resources)}catch(R){console.warn("Failed to parse config ".concat(o)),localStorage.setItem("raconf",JSON.stringify(C))}r.resources||(r.resources={}),t=r.resources}for(var c=0,s=Object.entries(t||{});c<s.length;c++){var l=Object(i.a)(s[c],2),u=l[0],d=l[1];if(d.hasOwnProperty("attributes")){d.columns=[],d.relationships=[],d.search_cols=[];var j,b=Object(S.a)(d.attributes);try{for(b.s();!(j=b.n()).done;){var f=j.value;if("string"==typeof f){var h={};h.name=f,d.columns.push(h)}else console.log("ignoring ".concat(f," in config"))}}catch(L){b.e(L)}finally{b.f()}for(var p=0,O=Object.entries(d.tab_groups||{});p<O.length;p++){var m=Object(i.a)(O[p],2),v=m[0],g=m[1],y={};y.name=v,y.fks=g.fks,y.direction=g.direction,"toone"===g.direction?y.target=g.target:(g.direction,y.target=g.resource),d.relationships.push(y)}}if(d.columns instanceof Array||d.relationships instanceof Array){d.type||(d.type=u),d.search_cols=[],r.resources[u].name=u;var x,w=Object(S.a)(d.columns);try{for(w.s();!(x=w.n()).done;){var k,_=x.value,P=Object(S.a)(d.relationships||[]);try{for(P.s();!(k=P.n()).done;){var J,T=k.value,A=Object(S.a)(T.fks||[]);try{for(A.s();!(J=A.n()).done;){var E=J.value;_.name===E&&(_.relationship=T,_.relationship.target_resource=r.resources[_.relationship.target])}}catch(L){A.e(L)}finally{A.f()}}}catch(L){P.e(L)}finally{P.f()}_.search&&d.search_cols.push(_)}}catch(L){w.e(L)}finally{w.f()}console.log("".concat(u," search cols"),d.search_cols)}}r||N();return r||N()},N=function(e){return console.log("Resetting conf",C),localStorage.setItem("raconf",JSON.stringify(C)),e&&window.location.reload(),C},J=(P(),P());var T=n(637),A=n.n(T),E=n(1022),R=n(1028),L=n(1053),I=n(1052),M=n(1038),H=n(1079),F=n(1075),B=n(1076),D=n(282),U=n(1060),W=n(1051),q=n(1064),G=n(1080),K=n(1039),z=n(510),V=n(1040),X=n(1062),Q=n(347),Y=n(937),Z=n(1029),$=n(240),ee=n.n($),te=n(621),ne=n.n(te),re=n(622),ae=n.n(re),oe=n(499),ce=n(935),ie=n(1056),se=n(1066),le=n(24),ue={position:"absolute",top:"50%",left:"50%",transform:"translate(-50%, -50%)",width:"75%",bgcolor:"background.paper",border:"2px solid #000",boxShadow:24,p:4,textAlign:"left"};function de(e){var t=e.label,n=e.content,a=e.resource_name,o=r.useState(!1),c=Object(i.a)(o,2),s=c[0],l=c[1];return Object(le.jsxs)("div",{children:[Object(le.jsxs)("span",{onClick:function(e){l(!0),e.stopPropagation()},className:"JoinedField",title:a,children:[t," "]}),Object(le.jsx)(se.a,{open:s,onClose:function(e){e.stopPropagation(),l(!1)},"aria-labelledby":"modal-modal-title","aria-describedby":"modal-modal-description",children:Object(le.jsxs)(ie.a,{sx:ue,children:[Object(le.jsx)(Q.a,{id:"modal-modal-title",variant:"h6",component:"h2",children:t}),Object(le.jsx)(Q.a,{id:"modal-modal-description",sx:{mt:2},children:n})]})})]})}var je=n(1058),be=n(1063),fe=n(641),he=(n(707),n(237)),pe=n(422),Oe=n(1032),me=P(),ve=[Object(le.jsx)(B.a,{source:"q",label:"Search",alwaysOn:!0})],ge=function(e){var t=e.column,r=t.component,a=t.style||{},o=Object(le.jsx)(E.a,{source:t.name,style:a},t.name);if(!r)return o;try{var c=Object(oe.a)((function(){return n.e(0).then(n.bind(null,1088))}),{resolveComponent:function(e){return e[r]}});return Object(le.jsx)(c,{column:t})}catch(i){alert("Custom component error"),console.error("Custom component error",i)}return o},ye=function(e){var t,r,a=e.column,o=e.join,c=Object(D.b)();c.attributes&&Object.assign(c,c.attributes);var i=o.name,l=(c.id,o.target),u=(Object(s.a)(),o.fks[0]),d=null===(t=me.resources[o.target])||void 0===t?void 0:t.user_key,j=Object(he.a)({type:"getOne",resource:l,payload:{id:c[u]}}),b=j.data,f=(j.loading,j.error,b||c[i]),h=null===(r=me.resources[o.target])||void 0===r?void 0:r.user_component,p=null===f||void 0===f?void 0:f.id;if(f&&h)p=function(e,t){try{var r=Object(oe.a)((function(){return n.e(0).then(n.bind(null,1088))}),{resolveComponent:function(t){return t["".concat(e)]}});return Object(le.jsx)(r,{instance:t})}catch(a){alert("Custom component error"),console.error("Custom component error",a)}return null}(h,f);else if((null===f||void 0===f?void 0:f.attributes)&&d){a.relationship.target_resource.columns.filter((function(e){return e.name==d}));p=Object(le.jsx)("span",{children:f.attributes[d]||f.id})}var O=Object(le.jsx)(Je,{instance:f,resource_name:o.target});return Object(le.jsx)(de,{label:p,content:O,resource_name:o.target},a.name)},xe=function(e,t){if(!t)return[];var n=t.filter((function(e){return"toone"===e.direction}));return e.map((function(e){if(e.hidden)return null;var t,r=Object(S.a)(n);try{for(r.s();!(t=r.n()).done;){var a,o=t.value,c=Object(S.a)(o.fks);try{for(c.s();!(a=c.n()).done;){var i=a.value;if(e.name==i)return Object(le.jsx)(ye,{column:e,join:o,label:e.label?e.label:e.name},e.name)}}catch(s){c.e(s)}finally{c.f()}}}catch(s){r.e(s)}finally{r.f()}return Object(le.jsx)(ge,{column:e,label:e.label?e.label:e.name,style:e.header_style},e.name)}))},Se=function(e){return Object(le.jsx)(fe.a,Object(j.a)({rowsPerPageOptions:[10,20,50,100],perPage:e.perPage||25},e))},we=function(e,t,n,r){console.log("Delete",n),e.delete(t,n).then((function(){r()})).catch((function(e){return alert("error")}))},ke=function(e){var t,n=e.column;e.resource;if("toone"==(null===(t=n.relationship)||void 0===t?void 0:t.direction)&&n.relationship.target){var r=me.resources[n.relationship.target].search_cols,a=Object(le.jsx)(je.a,{optionText:""},n.name);return r?0==r.length?console.warn("no searchable columns configured for ".concat(n.relationship.target)):a=Object(le.jsx)(je.a,{optionText:r[0].name},n.name):console.error("no searchable columns configured"),Object(le.jsx)(be.a,{source:n.name,label:"".concat(n.relationship.name," (").concat(n.name,")"),reference:n.relationship.target,children:a})}return Object(le.jsx)(B.a,{source:n.name})},_e=function(e){var t=e.record;return Object(le.jsx)("span",{children:t?"".concat(t.type?t.type+" ":""," #").concat(t.id," "):""})},Ce=function(e){var t=e.source,n=Object(D.b)();return n?Object(le.jsx)(Pe,{label:t,value:n[t]}):null},Pe=function(e){var t=e.label,n=e.value;return Object(le.jsxs)(M.a,{item:!0,xs:3,children:[Object(le.jsx)(Q.a,{variant:"body2",color:"textSecondary",component:"p",children:t}),Object(le.jsx)(Q.a,{variant:"body2",component:"p",children:n})]})},Ne=function(e){var t=e.columns,n=e.relationships,a=e.resource_name,o=e.id,c=Object(le.jsxs)(Q.a,{variant:"h5",component:"h5",style:{margin:"30px 0px 30px"},children:[a,Object(le.jsxs)("i",{style:{color:"#ccc"},children:[" #",o]})]});return Object(le.jsxs)(K.a,{children:[c,Object(le.jsx)(M.a,{container:!0,spacing:3,margin:5,m:40,children:t.map((function(e){return Object(le.jsx)(Ce,{source:e.name})}))}),Object(le.jsx)("hr",{style:{margin:"30px 0px 30px"}}),Object(le.jsx)(F.a,{tabs:Object(le.jsx)(z.a,{variant:"scrollable",scrollButtons:"auto"}),children:n.map((function(e){return"tomany"===e.direction?function(e,t,n){var a=Object(r.useState)(!0),o=Object(i.a)(a,2),c=(o[0],o[1]),l=Object(r.useState)(),u=Object(i.a)(l,2),d=(u[0],u[1]),j=Object(r.useState)(!1),b=Object(i.a)(j,2),f=(b[0],b[1]),h=Object(s.a)();Object(r.useEffect)((function(){h.getOne(e,{id:t}).then((function(e){var t=e.data;f(t.relationships),c(!1)})).catch((function(e){d(e),c(!1)}))}),[]);var p=me.resources[n.target];if(!p)return console.warn("".concat(e,": No resource conf for ").concat(p)),Object(le.jsx)("span",{});if(!(null===p||void 0===p?void 0:p.columns))return console.log("No target resource columns"),Object(le.jsx)("div",{});var O=p.columns.filter((function(t){var n;return(null===(n=t.relationship)||void 0===n?void 0:n.target)!==e})),m=null===p||void 0===p?void 0:p.relationships,v=xe(O,m);return n.source=e,Object(le.jsx)(H.a,{label:n.name,children:Object(le.jsx)(L.a,{pagination:Object(le.jsx)(Se,{perPage:p.perPage}),children:Object(le.jsx)(G.a,{reference:n.target,target:n,addLabel:!1,children:Object(le.jsxs)(I.a,{rowClick:"show",sort:"id",children:[v,Object(le.jsx)(R.a,{})]})})})})}(a,o,e):function(e,t,n){var a=Object(r.useState)(!0),o=Object(i.a)(a,2),c=(o[0],o[1]),l=Object(r.useState)(),u=Object(i.a)(l,2),d=(u[0],u[1]),j=Object(r.useState)(!1),b=Object(i.a)(j,2),f=b[0],h=b[1],p=Object(s.a)();return Object(r.useEffect)((function(){p.getOne(e,{id:t}).then((function(e){var t,r,a=e.data;return{rel_resource:null===(t=a[n.target])||void 0===t?void 0:t.data.type,rel_id:null===(r=a[n.target])||void 0===r?void 0:r.data.id}})).then((function(e){var t=e.rel_resource,n=e.rel_id;p.getOne(t,{id:n}).then((function(e){var t=e.data;return console.log(t),h(t)})).then((function(){return console.log(f)})),c(!1)})).catch((function(e){d(e),c(!1)}))}),[]),Object(le.jsx)(H.a,{label:n.name,children:Object(le.jsx)(Je,{instance:f})})}(a,o,e)}))})]})},Je=function(e){var t=e.instance,n=function(e){for(var t=0,n=Object.entries(null===me||void 0===me?void 0:me.resources);t<n.length;t++){var r=Object(i.a)(n[t],2),a=r[0];if(r[1].type===e)return a}return console.warn('No resource for type "'.concat(e)),me[e]}(null===t||void 0===t?void 0:t.type);if(!t||!n)return Object(le.jsx)("span",{});var r=me.resources[n],a=(null===r||void 0===r?void 0:r.columns)||[];null===r||void 0===r||r.relationships;return Object(le.jsxs)("div",{style:{left:"-16px",position:"relative"},children:[Object(le.jsxs)("div",{style:{textAlign:"right",width:"100%"},children:[Object(le.jsxs)(ce.a,{title:"edit",component:V.a,to:{pathname:"".concat(n,"/").concat(t.id)},label:"Link",children:[Object(le.jsx)(ne.a,{}),"Edit"]}),Object(le.jsxs)(ce.a,{title:"view",component:V.a,to:{pathname:"/".concat(n,"/").concat(t.id,"/show")},label:"Link",children:[Object(le.jsx)(ae.a,{}),"View"]})]}),Object(le.jsx)(M.a,{container:!0,title:"qsd",children:a.map((function(e){return Object(le.jsx)(Pe,{label:e.name,value:t.attributes[e.name]},e.name)}))})]})},Te=function(e){window.addEventListener("storage",(function(){return window.location.reload()}));var t=a.a.useState(),n=(Object(i.a)(t,2)[1],Object(r.useState)(me.resources[e.name])),o=Object(i.a)(n,2),c=o[0],l=(o[1],Object(r.useMemo)((function(){return e=c,function(t){var n=e.columns,r=e.relationships,a=xe(n,r),o=Object(s.a)(),c=Object(Y.a)(),i=[!1!==e.edit?Object(le.jsx)(R.a,{label:""},e.name):null,!1!==e.delete?Object(le.jsx)(Z.a,{onClick:function(e){e.stopPropagation()},render:function(e){return Object(le.jsx)(ee.a,{style:{fill:"#3f51b5"},onClick:function(n){return we(o,t.resource,e,c)}})}},e.name):null];return Object(le.jsx)(L.a,Object(j.a)(Object(j.a)({filters:ve,pagination:Object(le.jsx)(Se,{perPage:e.perPage}),sort:e.sort||""},t),{},{children:Object(le.jsxs)(I.a,{rowClick:"show",children:[a,i]})}))};var e}),[c])),d=Object(r.useMemo)((function(){return e=c,function(t){return Object(le.jsx)(q.a,Object(j.a)(Object(j.a)({},t),{},{children:Object(le.jsx)(W.a,{children:e.columns.map((function(t){return Object(le.jsx)(ke,{column:t,resource:e},t.name)}))})}))};var e}),[c]),b=Object(r.useMemo)((function(){return function(e){var t=e.columns;return function(e){Object(pe.a)();var n=Object(Y.a)(),r=Object(Oe.a)();return Object(le.jsx)(U.a,Object(j.a)(Object(j.a)({},e),{},{onFailure:function(t){r("edit",e.basePath,e.id),n()},children:Object(le.jsx)(W.a,{children:t.map((function(e){return Object(le.jsx)(ke,{column:e},e.name)}))})}))}}(c)}),[c]),f=Object(r.useMemo)((function(){return function(e){return function(t){var n=e.columns,r=e.relationships;return Object(le.jsx)(X.a,Object(j.a)(Object(j.a)({title:Object(le.jsx)(_e,{})},t),{},{children:Object(le.jsx)(Ne,{columns:n,relationships:r,resource_name:t.resource,id:t.id})}))}}(c)}),[c]);return Object(le.jsx)(u.a,Object(j.a)(Object(j.a)({},e),{},{list:l,edit:b,create:d,show:f}),e.name)},Ae=n(1035),Ee=n(936),Re=n(211),Le=function(){return Object(le.jsxs)(Ae.a,{children:[Object(le.jsx)(Re.b,{title:"Home"}),Object(le.jsxs)(Ee.a,{children:[Object(le.jsx)("center",{children:Object(le.jsx)("h1",{children:"Welcome to API Logic Server"})}),Object(le.jsx)("br",{}),Object(le.jsx)("h2",{children:"Automatic Admin App, Designed For"}),Object(le.jsxs)("ul",{children:[Object(le.jsxs)("li",{children:["Instant Business User Collaboration - Working Software ",Object(le.jsx)("i",{children:"Now"})]}),Object(le.jsx)("li",{children:"Back Office Data Maintenance"})]}),Object(le.jsx)("br",{}),Object(le.jsx)("h2",{children:"Key Features"}),Object(le.jsxs)("ul",{children:[Object(le.jsxs)("li",{children:[Object(le.jsx)("strong",{children:"Multi-page:"})," screen transitions"]}),Object(le.jsxs)("li",{children:[Object(le.jsx)("strong",{children:"Multi-table:"})," child grids, parent joins"]}),Object(le.jsxs)("li",{children:[Object(le.jsx)("strong",{children:"Logic aware:"})," multi-table derivations and constraints, extensible with Python events for email, messages, etc"]}),Object(le.jsxs)("li",{children:[Object(le.jsx)("strong",{children:"Customizable:"})," see ui/admin/admin.yaml.  Use SAFRS API for custom apps."]})]}),Object(le.jsx)("br",{}),Object(le.jsx)("h2",{children:"Resources"}),Object(le.jsxs)("ul",{children:[Object(le.jsx)("li",{children:Object(le.jsx)("a",{className:"custom",rel:"nofollow",href:"http://localhost:5656/api",target:"_blank",children:"Swagger"})}),Object(le.jsx)("li",{children:Object(le.jsx)("a",{className:"custom",rel:"nofollow",href:"https://github.com/valhuber/ApiLogicServer/blob/main/README.md/",target:"_blank",children:"API Logic Server Docs"})}),Object(le.jsx)("li",{children:Object(le.jsx)("a",{className:"custom",rel:"nofollow",href:"https://github.com/valhuber/ApiLogicServer/wiki/Working-with-the-Admin-App/",target:"_blank",children:"Admin App Customization Docs"})})]})]})]})},Ie=n(929),Me=n(1065),He=n(311),Fe=n(1048),Be=n(639),De=n(1072),Ue=n(1070),We=n(1057),qe=n(1069),Ge=n(1050),Ke=n(524),ze=Object(He.a)((function(e){return{widget:{border:"1px solid #3f51b5",marginRight:"1em",marginTop:"1em",marginBottom:"1em"},textInput:{width:"80%"}}})),Ve=function(){var e=[];try{e=JSON.parse(localStorage.getItem("raconfigs","{}"))}catch(c){}var t=r.useState(e&&e[0]),n=Object(i.a)(t,2),a=n[0],o=n[1];return Object(le.jsx)(De.a,{sx:{minWidth:120},children:Object(le.jsxs)(qe.a,{fullWidth:!0,children:[Object(le.jsx)(Ue.a,{id:"demo-simple-select-label",children:"Config"}),Object(le.jsx)(Ge.a,{labelId:"demo-simple-select-label",id:"demo-simple-select",value:a,label:"Configs",size:"small",onChange:function(e){o(e.target.value)},defaultValue:"30",children:e?Object.entries(e).map((function(e){return Object(le.jsx)(We.a,{value:"30",children:"Ten"})})):null})]})})},Xe=function(){var e,t=ze(),n=function(e){try{if(e){var t=JSON.parse(e);g(t.api_root)}b("#ddeedd"),localStorage.setItem("raconf",e),s||window.location.reload()}catch(n){b("red")}l(e)},a=localStorage.getItem("raconf")||JSON.stringify(N()),o=Object(r.useState)(a?JSON.stringify(JSON.parse(a),null,4):""),c=Object(i.a)(o,2),s=c[0],l=c[1],u=Object(r.useState)("black"),d=Object(i.a)(u,2),j=d[0],b=d[1],f=Object(r.useState)(!0),h=Object(i.a)(f,2),p=h[0],O=h[1],m=Object(r.useState)(null===(e=JSON.parse(a))||void 0===e?void 0:e.api_root),v=Object(i.a)(m,2),g=(v[0],v[1]);return Object(le.jsxs)("div",{children:[Object(le.jsxs)("div",{children:[Object(le.jsx)(Ve,{}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return n("")},color:"primary",children:"Clear"}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return n(JSON.stringify(N(),null,4))},color:"primary",children:"Reset"}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return window.location.reload()},color:"primary",children:"Apply"}),Object(le.jsx)(ce.a,{className:t.widget,onClick:function(){return localStorage.getItem("raconf"),void JSON.parse(localStorage.getItem("raconfigs","{}"))},color:"primary",children:"Save"}),Object(le.jsx)(Fe.a,{control:Object(le.jsx)(Me.a,{checked:p,onChange:function(e){O(e.target.checked)}}),label:"Auto Save Config"})]}),Object(le.jsx)("div",{children:Object(le.jsxs)(F.a,{children:[Object(le.jsx)(H.a,{label:"yaml",children:Object(le.jsx)(Be.a,{language:"yaml",value:Ke.dump(JSON.parse(s)),options:{theme:"vs-dark"},height:"1000px",style:{borderLeft:"8px solid ".concat(j)},onChange:function(e,t){return function(e,t){console.log(e);try{var r=Ke.load(e);n(JSON.stringify(r)),b("black")}catch(a){console.warn("Failed to process",e),b("red")}}(e)}})}),Object(le.jsx)(H.a,{label:"json",children:Object(le.jsx)(Ie.a,{variant:"outlined",minRows:3,style:{width:"80%",backgroundColor:"white"},value:JSON.stringify(JSON.parse(s),null,4),onChange:function(e){return n(e.target.value)}})})]})})]})},Qe=n(1054),Ye=n(51),Ze=n(299),$e=n(626),et=n(443),tt=n(627),nt=n(444),rt=n.n(nt),at=function(e){},ot=function(e){var t=Object(Ye.f)(Ze.b);return Object(le.jsxs)($e.a,Object(j.a)(Object(j.a)({},e),{},{children:[t.map((function(e){return Object(le.jsx)(et.a,{to:"/".concat(e.name),primaryText:e.options&&e.options.label||e.name,leftIcon:e.icon?Object(le.jsx)(e.icon,{}):Object(le.jsx)(rt.a,{}),onClick:at,sidebarIsOpen:true},e.name)})),Object(le.jsx)(tt.a,{})]}))},ct=function(e){return Object(le.jsx)(Qe.a,Object(j.a)(Object(j.a)({},e),{},{menu:ot}))},it=n(50),st=n(14),lt=n.n(st),ut=n(150),dt=n(253),jt=n(572),bt=n(451),ft=(n(138),n(344)),ht=n(310),pt=n(1061),Ot=P();var mt=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,t=arguments.length>1?arguments[1]:void 0;t.type,t.payload;return e},vt=function(e){for(var t=0,n=Object.entries(Ot.resources);t<n.length;t++){var r=Object(i.a)(n[t],2),a=r[0];if(r[1].type===e)return a}return!1},gt=function(e,t){var n,r,a,o,c=Object(ft.a)(e,t);if("CRUD_GET_ONE_SUCCESS"==t.type)return c;var s,l=new Set,u=Object(S.a)((null===(o=t.payload)||void 0===o?void 0:o.included)||[]);try{for(u.s();!(s=u.n()).done;){var d=s.value,j=vt(d.type);void 0!==d.type&&void 0!==d.id&&j&&(c.resources[j]||(c.resources[j]={}),c.resources[j][d.id]=d,l.add(j))}}catch(x){u.e(x)}finally{u.f()}var b,f=Object(S.a)(l);try{for(f.s();!(b=f.n()).done;)b.value}catch(x){f.e(x)}finally{f.f()}if(Array.isArray(null===(n=t.payload)||void 0===n?void 0:n.data)){var h=t.payload.data;Array.isArray(t.payload.included);var p,O=Object(S.a)(h);try{for(O.s();!(p=O.n()).done;){var m=p.value;if(m.relationships)for(var v=function(){var e,t,n=Object(i.a)(y[g],2),r=n[0],a=n[1],o=vt(null===(e=a.data)||void 0===e?void 0:e.type);o&&(Array.isArray(a.data)?m.relationships[r]=m[r]=a.data.map((function(e){return c.resources[o][e.id]})):(null===(t=a.data)||void 0===t?void 0:t.id)&&(m.relationships[r]=m[r]=c.resources[o][a.data.id]))},g=0,y=Object.entries(m.relationships);g<y.length;g++)v()}}catch(x){O.e(x)}finally{O.f()}}else null===(r=t.payload)||void 0===r||null===(a=r.data)||void 0===a||a.type;return c},yt=function(e){var t=e.authProvider,n=e.dataProvider,r=e.history,a=Object(ut.b)({admin:gt,router:Object(dt.b)(r),sReducer:mt}),o=lt.a.mark((function e(){return lt.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Object(it.a)([Object(pt.a)(n,t)].map(it.f));case 2:case"end":return e.stop()}}),e)})),c=Object(bt.a)(),i=ut.c,s=Object(ut.d)((function(e,t){return a(t.type!==ht.f?e:void 0,t)}),{},i(Object(ut.a)(c,Object(jt.a)(r))));return c.run(o),s},xt=n(148),St=n(638),wt=n.n(St),kt=Object(xt.b)(),_t=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,t=arguments.length>1?arguments[1]:void 0,n=t.type,r=t.payload;return"RA/CRUD_GET_LIST_SUCCESS"===n&&(console.log("bcR",n,r),console.log(e)),e},Ct=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{conf:{}},n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:f.a.fetchJson,r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"Content-Range",a=Object(h.a)(x,t);t.conf;return{getList:function(t,r){var o,c=t,i=r.pagination,s=i.page,l=i.perPage,u=J.resources[c],d=u.sort,j={"page[number]":s,"page[size]":l,"page[offset]":(s-1)*l,"page[limit]":l,sort:d||""};if((null===(o=r.filter)||void 0===o?void 0:o.q)&&"resources"in J){var f=u.columns.filter((function(e){return 1==e.search})).map((function(e){return e.name}));u.sort;j.filter=JSON.stringify(f.map((function(e){return{name:e,op:"like",val:"".concat(r.filter.q,"%")}})))}else Object.keys(r.filter||{}).forEach((function(e){j["filter[".concat(e,"]")]=r.filter[e]}));if(r.sort&&r.sort.field){var h="ASC"===r.sort.order?"":"-";j.sort="".concat(h).concat(r.sort.field)}var p=(J.resources[c].relationships||[]).map((function(e){return e.name}));j.include=p.join(",");var O="".concat(e,"/").concat(t,"?").concat(Object(b.stringify)(j));return n(O).then((function(e){var t=e.json,n=0;t.meta&&a.total&&(n=t.meta[a.total]),n=n||t.data.length;var r=new _(t),o=t.data.map((function(e){return r.unwrapData(e,p)}));return{data:o,included:t.included,total:n}})).catch((function(e){console.log("catch Error",e.body);var t=a.errorHandler;return Promise.reject(t(e))}))},getOne:function(t,r){var a=(J.resources[t].relationships||[]).map((function(e){return e.name})).join(","),o="".concat(e,"/").concat(t,"/").concat(r.id,"?include=").concat(a);return n(o).then((function(e){var t=e.json.data,n=t.id,r=t.attributes,a=t.relationships,o=t.type;return Object.assign(r,a,{type:o},{relationships:a},{attributes:Object(j.a)({},r)}),{data:Object(j.a)({id:n},r)}}))},getMany:function(t,r){t=t;var o="filter[id]="+JSON.stringify(r.ids),c="".concat(e,"/").concat(t,"?").concat(o);return n(c).then((function(e){var t=e.json;console.log("gtMany",t);var n=0;return t.meta&&a.total&&(n=t.meta[a.total]),n=n||t.data.length,{data:t.data.map((function(e){return Object.assign({id:e.id,type:e.type},e.attributes)})),total:n}}))},getManyReference:function(t,a){var o,c;console.log("GMR"),console.log(t,a.target);var i=a.pagination,s=i.page,l=i.perPage,u=a.sort,d=u.field,f=u.order,h={sort:JSON.stringify([d,f]),range:JSON.stringify([(s-1)*l,s*l-1]),filter_:JSON.stringify(Object(j.a)({},a.filter))},p=null===(o=a.target)||void 0===o?void 0:o.name,O="".concat(e,"/").concat(null===(c=a.target)||void 0===c?void 0:c.source,"/").concat(a.id,"/").concat(p,"?").concat(Object(b.stringify)(h));return n(O,{}).then((function(e){var t,n=e.headers,a=e.json;return n.has(r)||console.debug("The ".concat(r," header is missing in the HTTP Response. The simple REST data provider expects responses for lists of resources to contain this header with the total number of results to build the pagination. If you are using CORS, did you declare ").concat(r," in the Access-Control-Expose-Headers header?")),{data:a.data,total:null===(t=a.data)||void 0===t?void 0:t.length}}))},update:function(t,r){var o=J.resources[t].type,c=a.endpointToTypeStripLastLetters;for(var i in c)if(t.endsWith(c[i])){o=t.slice(0,-1*c[i].length);break}var s={data:{id:r.id,type:o,attributes:r.data}};return n("".concat(e,"/").concat(t,"/").concat(r.id),{method:a.updateMethod,body:JSON.stringify(s)}).then((function(e){var t=e.json.data,n=t.id,r=t.attributes;return{data:Object(j.a)({id:n},r)}})).catch((function(e){console.log("catch Error",e.body);var t=a.errorHandler;return Promise.reject(t(e))}))},updateMany:function(t,r){return Promise.all(r.ids.map((function(a){return n("".concat(e,"/").concat(t,"/").concat(a),{method:"PUT",body:JSON.stringify(r.data)})}))).then((function(e){return{data:e.map((function(e){return e.json.id}))}}))},create:function(t,r){var o=t,c=a.endpointToTypeStripLastLetters;for(var i in c)if(t.endsWith(c[i])){o=t.slice(0,-1*c[i].length);break}var s={data:{type:o,attributes:r.data}};return n("".concat(e,"/").concat(t),{method:"POST",body:JSON.stringify(s)}).then((function(e){var t=e.json.data,n=t.id,r=t.attributes;return{data:Object(j.a)({id:n},r)}})).catch((function(e){console.log("catch Error",e.body);var t=a.errorHandler;return Promise.reject(t(e))}))},delete:function(t,r){return n("".concat(e,"/").concat(t,"/").concat(r.id),{method:"DELETE",headers:new Headers({"Content-Type":"text/plain"})}).then((function(e){return{data:e.json}}))},deleteMany:function(t,r){return Promise.all(r.ids.map((function(r){return n("".concat(e,"/").concat(t,"/").concat(r),{method:"DELETE",headers:new Headers({"Content-Type":"text/plain"})})}))).then((function(e){return{data:e.map((function(e){return e.json.id}))}}))},getResources:function(){return J?Promise.resolve({data:J}):n("".concat(e,"/schema"),{method:"GET"}).then((function(e){var t=e.json;return localStorage.setItem("raconf",JSON.stringify(t)),{data:t}})).catch((function(){return{data:{}}}))}}}(P().api_root,{}),Pt=function(){return Promise.resolve()},Nt=function(){var e=Object(r.useState)(!1),t=Object(i.a)(e,2),n=t[0],a=t[1],o=Object(s.a)();return Object(r.useEffect)((function(){o.getResources().then((function(e){var t=Object.keys(e.data.resources).map((function(e){return{name:e}}));a(t)})).catch((function(e){console.warn(e),a([])}))}),[]),!1===n?Object(le.jsx)("div",{children:"Loading..."}):Object(le.jsx)(Ye.a,{store:yt({authProvider:Pt,dataProvider:o,history:kt}),children:Object(le.jsxs)(l.a,{layout:ct,children:[Object(le.jsx)(u.a,{name:"Home",show:Le,list:Le,options:{label:"Home"},icon:A.a}),Object(le.jsx)(u.a,{name:"Configuration",show:Xe,list:Xe,options:{label:"Configuration"},icon:wt.a}),n.map((function(e){return Object(le.jsx)(Te,{name:e.name},e.name)}))]})})},Jt=function(){return Object(le.jsx)(d.a,{dataProvider:Ct,customReducers:{admin2:_t},children:Object(le.jsx)(Nt,{})})},Tt=function(e){e&&e instanceof Function&&n.e(84).then(n.bind(null,1164)).then((function(t){var n=t.getCLS,r=t.getFID,a=t.getFCP,o=t.getLCP,c=t.getTTFB;n(e),r(e),a(e),o(e),c(e)}))};c.a.render(Object(le.jsx)(Jt,{}),document.getElementById("root")),Tt()}},[[926,4,5]]]);
//# sourceMappingURL=main.cf97d91c.chunk.js.map