# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMove, self).default_get(default_fields)
        branch_id = self._context.get('branch_id')
        if branch_id:
            if 'branch_id' in default_fields:
                res.update({'branch_id': branch_id})
            elif self.env.user.branch_id:
                if 'branch_id' in default_fields:
                    res.update({'branch_id': self.env.user.branch_id.id})
        return res

    branch_id = fields.Many2one('res.branch', string="الفرع")

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        selected_brach = self.branch_id
        if selected_brach:
            user_id = self.env['res.users'].browse(self.env.uid)
            user_branch = user_id.sudo().branch_id
            if user_branch and user_branch.id != selected_brach.id:
                raise UserError("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that.") 


    @api.model
    def create(self, vals):
        print ("create move")
        print(self)
        print(vals)
        context_keys = self.env.context.keys()
        print("Context keys:", context_keys)

        if 'branch_id' not in vals:
            if self.env.context.get('default_payment_id'):
                payment = self.env['account.payment'].browse(self.env.context.get('default_payment_id'))
                if payment.branch_id:
                    vals['branch_id'] = payment.branch_id.id
                    print("Branch ID set from default_payment_id: ", payment.branch_id.id)
           
            if not vals.get('branch_id') and self.env.user.branch_id:
                    vals['branch_id'] = self.env.user.branch_id.id
                    print("Branch ID set from user branch: ", self.env.user.branch_id.id)

        return super(AccountMove, self).create(vals)


    def write(self, vals):
        print ("updat move")
        print(self)
        print(vals)
        if 'branch_id' not in vals:
            for move in self:
                if move.payment_id and move.payment_id.branch_id:
                    vals['branch_id'] = move.payment_id.branch_id.id
                    print("Branch ID set from payment_id: ", move.payment_id.branch_id.id)
                
                
                if not vals.get('branch_id') and self.env.user.branch_id:
                    vals['branch_id'] = self.env.user.branch_id.id
                    print("Branch ID set from user branch: ", self.env.user.branch_id.id)

        return super(AccountMove, self).write(vals)




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountMoveLine, self).default_get(default_fields)
        branch_id = self._context.get('branch_id')
        if branch_id:
            if 'branch_id' in default_fields:
                res.update({'branch_id': branch_id})
            elif self.env.user.branch_id:
                if 'branch_id' in default_fields:
                    res.update({'branch_id': self.env.user.branch_id.id})
            if self.move_id.branch_id :
                if 'branch_id' in default_fields:
                    res.update({'branch_id': self.move_id.branch_id.id})
        return res

    branch_id = fields.Many2one('res.branch', string="الفرع",related="move_id.branch_id",store=True)
