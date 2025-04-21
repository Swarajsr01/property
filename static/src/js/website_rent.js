/** @odoo-module **/
console.log("file running")
import publicWidget from "@web/legacy/js/public/public_widget";
//import { renderToElement } from "@web/core/utils/render";
//import { useRef, useState } from "@odoo/owl";

publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    selector: '#wrap', events: {
        'change #from_date': '_onChangeCalculate_total_days',
        'change #to_date': '_onChangeCalculate_total_days',
        'click #add_btn': '_onClickRow_line_add',
        'click #remove_line': '_onClickRow_line_remove',
        'change #property': '_onChangeProperty_id',
        'change #type': '_onChangeType',
        'change #total_days': '_onChangeType',
    },
     _onClickRow_line_add: function(ev){
                var flag = 0;
                const section = this.el.querySelector('#line-section');
                const allDivs = section.querySelectorAll('div');
                allDivs.forEach(div => {
                    const select = div.querySelector('#property');

                    if (select.value == "") {
                       flag = 1;
                    }
                });
                if (flag == 0){
                    const line = allDivs[allDivs.length - 1];
                    const test = line.getAttribute('id');
                    const clone = line.cloneNode(true);
                    clone.querySelectorAll("input").forEach(input => input.value = "");
                    const idMatch = line.id.match(/(.*_)(\d+)/);
                    let nextId = "";
                    if (idMatch) {
                        const base = idMatch[1];
                        const num = parseInt(idMatch[2]) + 1;
                        nextId = base + num;
                    }
                    clone.setAttribute("id", nextId);
                    const br = document.createElement("br");
                    section.appendChild(clone);
                }
                else{
                    const modal = this.el.querySelector('#myModal');
                    modal.querySelector('#message').innerText='You want to fill unfilled line first.'+
                    'After that try to create new line'
                    modal.style.display = "block";
                }
     },
     _onClickRow_line_remove: function(ev){
                  const section = this.el.querySelector('#line-section');
                  const allDivs = section.querySelectorAll('div');
                  if (allDivs.length > 1){
                      const current_button = ev.currentTarget;
                      var parentDiv = current_button.parentElement;
                      parentDiv.remove();
                  }
                  else{
                       const modal = this.el.querySelector('#myModal');
                       modal.querySelector('#message').innerText='At least one property want to create rent/lease order'
                       modal.style.display = "block";
                  }
     },
     _onChangeType: function(ev){
                    const section = this.el.querySelector('#line-section');
                    const parentDivIds = Array.from(section.querySelectorAll('#property')).map(el => {
                        return el.closest('div')?.id;
                    });
                    const type = this.el.querySelector('#type').value;
                    for (const id of parentDivIds) {
                        const current_parent_div =  this.el.querySelector(`#${id}`);
                        const current_div_property =  current_parent_div.querySelector('#property').value;
                        const total_days = this.el.querySelector('#total_days').value;
                        if(current_div_property != ""){
                            fetch('/get/property/amount', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-Requested-With': 'XMLHttpRequest',
                                },
                                body: JSON.stringify({ jsonrpc: "2.0",
                                    method: "call",
                                    params: { property_id: current_div_property,
                                              type: type,
                                             }
                                }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                current_parent_div.querySelector('#amount').value = data.result.response_value;
                                current_parent_div.querySelector('#total_amount').value =
                                data.result.response_value * parseInt(total_days);
                            })
                        }
                    }
     },
     _onChangeProperty_id: function(ev){
                  const current_selection = ev.currentTarget;
                  const current_property_id =  current_selection.value;
                  const current_parent_div = current_selection.parentElement;
                  const section = this.el.querySelector('#line-section');
                  const properties = Array.from(section.querySelectorAll('#property'));
                  const values = properties.slice(0, -1).map(el => el.value);
                  if (values.includes(current_property_id)){
//                      current_parent_div.querySelector('#property').value = "";
                      current_parent_div.querySelector('#amount').value = "";
                      current_parent_div.querySelector('#total_amount').value = "";
                      const modal = this.el.querySelector('#myModal');
                      modal.querySelector('#message').innerText = 'property already exist'
                      modal.style.display = "block";
                  }
                  else{
                      const total_days = this.el.querySelector('#total_days').value;
                      const type = this.el.querySelector('#type').value;
                      if(current_property_id != ""){
                          fetch('/get/property/amount', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-Requested-With': 'XMLHttpRequest',
                                },
                                body: JSON.stringify({ jsonrpc: "2.0",
                                    method: "call",
                                    params: { property_id: current_property_id,
                                              type: type,
                                             }
                                }),
                          })
                          .then(response => response.json())
                          .then(data => {
                                current_parent_div.querySelector('#amount').value = data.result.response_value;
                                current_parent_div.querySelector('#total_amount').value =
                                data.result.response_value * parseInt(total_days);
                          })
                      }
                      else{
                           current_parent_div.querySelector('#amount').value = "";
                           current_parent_div.querySelector('#total_amount').value = "";
                      }
                  }
     },
    _onChangeCalculate_total_days: function(ev){
                var from_date = this.$el.find('#from_date').val()
                var to_date = this.$el.find('#to_date').val()
                var days = (new Date(to_date) - new Date(from_date))/(1000 * 60 * 60 * 24);
                if (days >= 0) {
                    this.$el.find('#total_days').val(days+1).trigger('change');
                }
                else {
                    this.$el.find('#total_days').val("");
                    const modal = this.el.querySelector('#myModal');
                    modal.querySelector('#message').innerText = 'To date cannot be earlier than From date.'
                    modal.style.display = "block";
                }
    },
});

