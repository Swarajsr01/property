/** @odoo-module **/

import { PosGlobalState } from 'point_of_sale.models';
import Registries from 'point_of_sale.Registries';

const PosCategoryDiscountState = (PosGlobalState) =>
    class extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(loadedData);

            const configParams = loadedData['ir.config_parameter'] || [];

            // Extract and parse values
            let selectedCategoryIds = [];
            let discountAmount = 0;

            if (configParams['res.config.settings.selected_category_ids']) {
                selectedCategoryIds = JSON.parse(configParams['res.config.settings.selected_category_ids']);
            }
            if (configParams['res.config.settings.category_wise_discount_amount']) {
                discountAmount = parseFloat(configParams['res.config.settings.category_wise_discount_amount']);
            }

            this.config.category_discount_config = {
                selected_category_ids: selectedCategoryIds,
                category_wise_discount_amount: discountAmount,
            };
        }
    };

Registries.Model.extend(PosGlobalState, PosCategoryDiscountState);
