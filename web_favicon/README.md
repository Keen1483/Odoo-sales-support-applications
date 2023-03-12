Le override du web title sur odoo ne fonctionne
pas avec le xpath:
<template id="custom_favicon" inherit_id="web.layout" name="Custom Favicon" priority="17">
     <xpath expr="//head//link" position="after">
         <link type="image/x-icon" rel="shortcut icon" t-att-href="x_icon or '/web_favicon/static/src/img/favicon.ico'"/>
     </xpath>
 </template>

Pour ce fait, procédez comme suit:

1. Ouvrir le fichier:
    web/static/src/js/chrome/abstract_web_client.js
   
2.  Modifier la ligne:
    this.set('title_part', {"zopenerp": "Odoo"});
    à:
    this.set('title_part', {"zopenerp": "Votre titre"});