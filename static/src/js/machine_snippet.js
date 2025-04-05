/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";


publicWidget.registry.machine_snippet_card = publicWidget.Widget.extend({
    selector:'.machine_snippet_card',
    start: function(){
        var self = this
        jsonrpc('/machine_snippet').then(function(data){
              data[0].is_active = true
              self.$el.find('#carousel_id').html(renderToElement("machine_management.machine_snippet_carousel",{data: data}))
        })
    },
});
