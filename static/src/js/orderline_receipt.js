/** @odoo-module **/

import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(Orderline.prototype, {
    setup() {
        super.setup?.();
        this.pos = usePos();
    },
    get productLine() {
        const renderedLine = this.props.line;
        const currentOrder = this.pos.get_order();
        const realOrderLine = currentOrder.get_orderlines()
            .find((line) => line.get_product().display_name.split('(')[0].trim() ===
            renderedLine.productName.split('(')[0].trim());
        if (!realOrderLine) {
            return 0;
        }
        const product = realOrderLine.get_product();
        return isNaN(product.product_quality) ? 0 : parseInt(product.product_quality) || 0;
    },
});
