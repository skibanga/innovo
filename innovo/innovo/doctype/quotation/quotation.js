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
    frm.refresh_field('Product');
}

frappe.ui.form.on('Quotation', {
    validate: function(frm) {
        update_totals(frm);
    },
    items_on_form_rendered: function(frm) {
        update_totals(frm);
    },
    items_add: function(frm) {
        update_totals(frm);
    },
    items_remove: function(frm) {
        update_totals(frm);
    }
});

function update_totals(frm) {
    let total_quantity = 0;
    let total_amount = 0;

    (frm.doc.items || []).forEach(row => {
        total_quantity += flt(row.quantity);
        total_amount += flt(row.amount);
    });

    frm.set_value('total_quantity', total_quantity);
    frm.set_value('total_amount', total_amount);
}
