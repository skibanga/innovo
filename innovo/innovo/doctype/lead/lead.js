// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lead", {
	// refresh: function(frm) {

	// }
	first_name: function (frm) {
		cust_name(frm);
	},
	middle_name: function (frm) {
		cust_name(frm);
	},
	last_name: function (frm) {
		cust_name(frm);
	},
});

function cust_name(frm) {
	if (frm.doc.first_name) {
		if (frm.doc.middle_name) {
			if (frm.doc.last_name) {
				frm.set_value("full_name", frm.doc.first_name + " " + frm.doc.middle_name + " " + frm.doc.last_name)
			}
			else {
				frm.set_value("full_name", frm.doc.first_name + " " + frm.doc.middle_name)
			}
		}
		else {
			if (frm.doc.last_name) {
				frm.set_value("full_name", frm.doc.first_name + " " + frm.doc.last_name)
			}
			else {
				frm.set_value("full_name", frm.doc.first_name)
			}
		}
	}
	else {
		if (frm.doc.middle_name) {
			if (frm.doc.last_name) {
				frm.set_value("full_name", frm.doc.middle_name + " " + frm.doc.last_name)
			}
			else {
				frm.set_value("full_name", frm.doc.middle_name)
			}
		}
		else {
			if (frm.doc.last_name) {
				frm.set_value("full_name", frm.doc.last_name)
			}
			else {
				frm.set_value("full_name", "")
			}
		}
	}
};

// frappe.ui.form.on("Lead", {
//     refresh: function(frm) {
//         const color_map = {
//             "Lead": "yellow",
//             "Prospect": "blue",
//             "Customer": "green"
//         };

//         const status = frm.doc.status;
//         const color = frappe.ui.color.get(color_map[status] || "gray");

//         if (status && frm.fields_dict.status) {
//             // Add badge styling
//             frm.fields_dict.status.$wrapper.css({
//                 "background-color": color,
//                 "color": "#fff",
//                 "padding": "4px 8px",
//                 "border-radius": "6px",
//                 "display": "inline-block",
//                 "font-weight": "bold"
//             });
//         }
//     }
// });

