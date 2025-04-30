/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";

PosStore.prototype._loadProducts = async function () {
    await this._super();

    // Add 'Custom' label to every product
    for (let product of this.db.get_product_by_id_list(this.db.product_by_id)) {
        product.custom_label = "Custom";
    }
};

