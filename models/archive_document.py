from odoo import models, fields, api

class ArchiveDocument(models.Model):
    _name = 'archive.document'
    _description = 'الوثائق الأرشيفية'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string='عنوان الوثيقة')
    reference = fields.Char('الرقم المرجعي')
    folder_id = fields.Many2one('archive.folder', required=True, string='مجلد الأرشيف')
    date = fields.Date('تاريخ الوثيقة', default=fields.Date.context_today)
    description = fields.Text('وصف الوثيقة')
    physical_location = fields.Char('الموقع الفعلي')
    digital_copy = fields.Binary('نسخة رقمية')
    filename = fields.Char('اسم الملف')
    company_id = fields.Many2one(related='folder_id.company_id', store=True)
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('archived', 'مؤرشف'),
        ('destroyed', 'تم التدمير')
    ], default='draft', tracking=True)
    archive_date = fields.Datetime('تاريخ الأرشفة')
    archived_by = fields.Many2one('res.users', 'مؤرشف بواسطة')
    related_model = fields.Char('النموذج المرتبط')
    related_id = fields.Integer('معرف السجل المرتبط')

    def action_archive(self):
        self.write({
            'state': 'archived',
            'archive_date': fields.Datetime.now(),
            'archived_by': self.env.user.id
        })

    def action_link_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'ربط بسجل موجود',
            'res_model': 'archive.link.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_document_id': self.id}
        }