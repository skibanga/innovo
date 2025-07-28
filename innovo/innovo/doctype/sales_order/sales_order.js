// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Details Table', {
    quantity: function(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    }
});

function calculate_row_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    row.amount = (row.quantity || 0) * (row.rate || 0);
    frm.refresh_field('items');
}
