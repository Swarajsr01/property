/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    selector: '#wrap', events: {
        'change #from_date': '_onChangeCalculate_total_days',
        'change #to_date': '_onChangeCalculate_total_days',
        'click #add_btn': '_onClickRow_line_add',
        'click #remove_line': '_onClickRow_line_remove',
        'change .property': '_onChangeProperty_id',
        'change #type': '_onChangeType',
        'change #total_days': '_onChangeType',
        'click #submit_rent': '_onClickSubmit_rent',
    },
     _onClickRow_line_add: function(ev){
                var flag = 0;
                const section = this.el.querySelector('#line-section');
                const all_divs = section.querySelectorAll('div');
                all_divs.forEach(div => {
                    const property = div.querySelector('.property');
                    if (property.value == "") {
                       flag = 1;
                    }
                });
                if (flag == 0){
                    const last_div = all_divs[all_divs.length - 1];
                    const clone = last_div.cloneNode(true);
                    clone.querySelectorAll("input").forEach(input => input.value = "");
                    const idMatch = last_div.id.match(/(.*_)(\d+)/);
                    let nextId = "";
                    if (idMatch) {
                        const base = idMatch[1];
                        const num = parseInt(idMatch[2]) + 1;
                        nextId = base + num;
                    }
                    clone.setAttribute("id", nextId);
                    section.appendChild(clone);
                }
                else{
                    this._showModalMessage('You want to fill unfilled line first. After that try to create new line');
                }
     },

     _onClickRow_line_remove: function(ev){
                  const section = this.el.querySelector('#line-section');
                  const all_divs = section.querySelectorAll('div');
                  if (all_divs.length > 1){
                      const current_button = ev.currentTarget;
                      var parent_div = current_button.parentElement;
                      parent_div.remove();
                  }
                  else{
                       this._showModalMessage('At least one property want to create rent/lease order');
                  }
     },

     _onClickSubmit_rent: function(ev){
                   var flag = 1;
                   var msg = ""
                   const form = this.el.querySelector('#website_form');
                   const section = this.el.querySelector('#line-section');
                   const properties_div = Array.from(section.querySelectorAll('.property')).map(el => {
                        return el.closest('div')?.id;
                    });
                   if (properties_div.length == 1){
                        const existing_div = this.el.querySelector(`#${properties_div[0]}`)
                        if((existing_div.querySelector('.property').value) == ""){
                              flag = 0;
                              msg = "At least one property want to create rent/lease order."
                        }
                   }
                   if ((form.querySelector('#total_days').value) == ""){
                        flag = 0;
                        msg = "Select valid dates,without from and to date.We can't create rent order."
                   }
                   if (flag == 1){
                        const properties_array = []
                        for (const id of properties_div){
                            const property_value = this.el.querySelector(`#${id} .property`).value;
                            var property_id = parseInt(property_value)
                            if (!isNaN(property_id)) {
                                 properties_array.push(property_id);
                            }
                        }
                        fetch('/property/rent/order', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-Requested-With': 'XMLHttpRequest',
                            },
                            body: JSON.stringify({ jsonrpc: "2.0",
                                method: "call",
                                params: { from_date: form.querySelector('#from_date').value,
                                          to_date: form.querySelector('#to_date').value,
                                          total_days: form.querySelector('#total_days').value,
                                          type: form.querySelector('#type').value,
                                          property_ids: properties_array,
                                         }
                            }),
                        })
                        .then(response => response.json())
                        .then(data => {
                              if (data.result.message) {
                                    this._showModalMessage(data.result.message);
                              }
                              else if(data.result.redirect_url){
                                    window.location.href = data.result.redirect_url;
                              }
                        })
                   }
                   else{
                        this._showModalMessage(msg);
                   }
     },

     _onChangeType: function(ev){
                    const section = this.el.querySelector('#line-section');
                    const parent_div_ids = Array.from(section.querySelectorAll('.property')).map(el => {
                        return el.closest('div')?.id;
                    });
                    const type = this.el.querySelector('#type').value;
                    for (const id of parent_div_ids) {
                        const current_parent_div =  this.el.querySelector(`#${id}`);
                        const property_id =  current_parent_div.querySelector('.property').value;
                        const total_days = this.el.querySelector('#total_days').value;
                        if(property_id != ""){
                              this._fetchPropertyAmount(current_parent_div, property_id, type, total_days)
                        }
                    }
     },

     _onChangeProperty_id: function(ev){
                  const current_selection = ev.currentTarget;
                  const current_property_id =  current_selection.value;
                  const current_parent_div = current_selection.parentElement;
                  const section = this.el.querySelector('#line-section');
                  const properties = Array.from(section.querySelectorAll('.property'));
                  const values = properties.filter(el => el !== current_selection).map(el => el.value);
                  if (values.includes(current_property_id)){
                      current_parent_div.querySelector('.property').value = "";
                      current_parent_div.querySelector('#amount').value = "";
                      current_parent_div.querySelector('#total_amount').value = "";
                      this._showModalMessage('property already exist');
                  }
                  else{
                      const total_days = this.el.querySelector('#total_days').value;
                      const type = this.el.querySelector('#type').value;
                      if(current_property_id != ""){
                           this._fetchPropertyAmount(current_parent_div, current_property_id, type, total_days)
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
                    this.$el.find('#total_days').val("").trigger('change');
                    this._showModalMessage('To date cannot be earlier than From date.')
                }
    },

    _showModalMessage: function(messageText){
                const modal = this.el.querySelector('#myModal');
                if (modal){
                    modal.querySelector('#message').innerText = messageText;
                    modal.style.display = "block";
                }
    },

    _fetchPropertyAmount: function(parent_div, property_id, type, total_days){
                fetch('/get/property/amount', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({ jsonrpc: "2.0",
                        method: "call",
                        params: { property_id: property_id,
                                  type: type,
                                 }
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    parent_div.querySelector('#amount').value = data.result.response_value;
                    if(total_days){
                        parent_div.querySelector('#total_amount').value =
                        data.result.response_value * parseInt(total_days);
                    }
                    else{
                        parent_div.querySelector('#total_amount').value = "";
                    }
                })
    }
});
