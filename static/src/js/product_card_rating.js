/** @odoo-module **/

import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype, {
    get PriorityStar(){
        const star = parseInt(this.props.product.product_quality)
        return isNaN(star) ? 0 : star;
    }
});