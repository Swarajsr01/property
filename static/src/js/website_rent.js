/** @odoo-module **/
console.log("file running")
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    selector: '#wrap', events: {
        'change #from_date': '_onChangeCalculate_total_days',
        'change #to_date': '_onChangeCalculate_total_days',
        'click #add_btn': '_onClickRow_line_add',
        'click #remove_line': '_onClickRow_line_remove',
        'change #property': '_onChangeProperty_amount',
    },
     _onClickRow_line_add: function(ev){
                const section = this.el.querySelector('#line-section');
                const allDivs = section.querySelectorAll('div');
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
     },

     _onClickRow_line_remove: function(ev){
                  const current_button = ev.currentTarget;
                  var parentDiv = current_button.parentElement;
                  console.log(parentDiv)
                  parentDiv.remove();
     },









     _onChangeProperty_amount: function(ev){
                  const current_selection = ev.currentTarget;
                  const current_property_id =  current_selection.value;
                  console.log(current_property_id)
                  var parentDiv = current_selection.parentElement;
                  console.log(parentDiv)
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
