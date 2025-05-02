/** @odoo-module **/

console.log("qwertyuiokjhgfdsdfghn")

import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
//import { usePos } from "@point_of_sale/app/store/pos_hook";
//import { onMounted } from "@odoo/owl";
//
patch(Orderline.prototype, {
     setup() {
         super.setup();
         console.log(this.props)
         console.log(this.props.product)
//         this.pos = usePos();
//         onMounted(() => {
////            console.log(this.props)
////            console.log(this.props.line)
//
//        });
     },
});

