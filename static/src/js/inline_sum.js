/** @odoo-module **/
console.log("file running")
import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";
import { useRef, useState } from "@odoo/owl";


//
//console.log("🔥 JS file is running without odoo.define");

//window.addEventListener('DOMContentLoaded', function () {
//    console.log("✅ DOM fully loaded, now running function");
//    const dateInput = document.getElementById('from_date');
//    if (!dateInput) {
//        console.log("teste")
//        const today = new Date();
//        const yyyy = today.getFullYear();
//        const mm = String(today.getMonth() + 1).padStart(2, '0');
//        const dd = String(today.getDate()).padStart(2, '0');
//        dateInput.value = `${yyyy}-${mm}-${dd}`;
//    }
//});


publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    selector: '#wrap', events: {
        'change #from_date': '_onChangeCalculate_total_days',
        'change #to_date': '_onChangeCalculate_total_days',
        'click #add_btn': '_onClickRow_line_add',

    },
    _onClickRow_line_add: function(ev){
                console.log("test");
                alert("2345");
                 const section = this.el.querySelector('#line-section');
                const line = section.querySelector("#order_line");
                const clone = line.cloneNode(true);
                clone.querySelectorAll("input").forEach(input => input.value = "");
                const br = document.createElement("br");
                section.appendChild(br);
                section.appendChild(clone);

     },
    _onChangeCalculate_total_days: function(ev){
                var from_date = this.$el.find('#from_date').val()
                var to_date = this.$el.find('#to_date').val()
                var days = (new Date(to_date) - new Date(from_date))/(1000 * 60 * 60 * 24);
                if (days > 0) {
                    this.$el.find('#total_days').val(days+1);
                }
                else {
                    alert("To date cannot be earlier than From date.");
                    this.$el.find('#total_days').val("");
                }
    },
});
