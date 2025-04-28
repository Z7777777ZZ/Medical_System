from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from diagnosis.models.prescription import Prescription, Medicine, PrescriptionDetail
from app import db
import logging

api = Namespace('prescription', description='处方管理操作')

# 定义数据模型
medicine_model = api.model('Medicine', {
    'id': fields.Integer(required=True, description='药品ID'),
    'name': fields.String(required=True, description='药品名称'),
    'specification': fields.String(required=True, description='规格'),
    'price': fields.Float(required=True, description='价格'),
    'stock': fields.Integer(required=True, description='库存'),
    'description': fields.String(required=False, description='描述')
})

medicine_detail_model = api.model('MedicineDetail', {
    'medicineId': fields.Integer(required=True, description='药品ID'),
    'quantity': fields.Integer(required=True, description='数量'),
    'usage': fields.String(required=False, description='用法用量')
})

prescription_model = api.model('Prescription', {
    'id': fields.Integer(readonly=True, description='处方ID'),
    'patientId': fields.Integer(required=True, description='患者ID'),
    'doctorId': fields.Integer(required=True, description='医生ID'),
    'date': fields.DateTime(required=False, description='处方日期'),
    'medicines': fields.List(fields.Nested(medicine_detail_model), required=True, description='药品列表'),
    'instructions': fields.String(required=False, description='医嘱'),
    'status': fields.String(required=False, description='状态')
})

@api.route('/medicines')
class MedicineList(Resource):
    @api.doc('获取所有药品')
    @api.marshal_list_with(medicine_model)
    # @jwt_required()  # 暂时注释掉以便测试
    def get(self):
        """获取所有药品列表"""
        try:
            medicines = Medicine.query.all()
            return [m.to_dict() for m in medicines]
        except Exception as e:
            logging.error(f"获取药品列表失败: {str(e)}")
            api.abort(500, f"获取药品列表失败: {str(e)}")

@api.route('/medicines/<int:medicine_id>')
class MedicineDetail(Resource):
    @api.doc('获取药品详情')
    @api.marshal_with(medicine_model)
    @jwt_required()
    def get(self, medicine_id):
        """获取药品详情"""
        medicine = Medicine.query.get_or_404(medicine_id)
        return medicine.to_dict()

@api.route('')
class PrescriptionList(Resource):
    @api.doc('创建处方')
    @api.expect(prescription_model)
    @jwt_required()
    def post(self):
        """创建新处方"""
        data = request.json
        
        prescription = Prescription(
            patient_id=data['patientId'],
            doctor_id=data['doctorId'],
            instructions=data.get('instructions', ''),
            status=data.get('status', 'pending')
        )
        
        db.session.add(prescription)
        db.session.flush()  # 获取新处方ID
        
        # 添加处方明细
        for med in data['medicines']:
            detail = PrescriptionDetail(
                prescription_id=prescription.prescription_id,
                medicine_id=med['medicineId'],
                quantity=med['quantity'],
                instructions=med.get('usage', '')
            )
            db.session.add(detail)
        
        db.session.commit()
        
        # 返回完整的处方信息
        result = prescription.to_dict()
        # 补充药品信息
        details = PrescriptionDetail.query.filter_by(prescription_id=prescription.prescription_id).all()
        medicines_list = []
        
        for detail in details:
            medicine = Medicine.query.get(detail.medicine_id)
            if medicine:
                med_dict = {
                    'id': medicine.medicine_id,
                    'name': medicine.name,
                    'specification': medicine.specification,
                    'price': medicine.price,
                    'quantity': detail.quantity,
                    'usage': detail.instructions
                }
                medicines_list.append(med_dict)
        
        result['medicines'] = medicines_list
        return result, 201

    @api.doc('获取处方列表')
    @api.param('patientId', '患者ID')
    @jwt_required()
    def get(self):
        """获取处方列表，可按患者ID过滤"""
        patient_id = request.args.get('patientId')
        query = Prescription.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        
        prescriptions = query.all()
        result = []
        
        for p in prescriptions:
            p_dict = p.to_dict()
            # 查询处方明细
            details = PrescriptionDetail.query.filter_by(prescription_id=p.prescription_id).all()
            medicines_list = []
            
            for detail in details:
                # 获取药品信息
                medicine = Medicine.query.get(detail.medicine_id)
                if medicine:
                    med_dict = medicine.to_dict()
                    med_dict['quantity'] = detail.quantity
                    med_dict['usage'] = detail.instructions
                    medicines_list.append(med_dict)
            
            p_dict['medicines'] = medicines_list
            result.append(p_dict)
        
        return result

@api.route('/<int:prescription_id>')
class PrescriptionDetailResource(Resource):  # 改名避免与模型类冲突
    @api.doc('获取处方详情')
    # @jwt_required()  # 暂时注释掉以便测试
    def get(self, prescription_id):
        """获取处方详情"""
        try:
            prescription = Prescription.query.get_or_404(prescription_id)
            
            # 手动获取处方详情和药品信息
            result = prescription.to_dict()
            # 查询处方明细
            details = PrescriptionDetail.query.filter_by(prescription_id=prescription.prescription_id).all()
            medicines_list = []
            
            for detail in details:
                # 获取药品信息
                medicine = Medicine.query.get(detail.medicine_id)
                if medicine:
                    med_dict = medicine.to_dict()
                    med_dict['quantity'] = detail.quantity
                    med_dict['usage'] = detail.instructions
                    medicines_list.append(med_dict)
            
            result['medicines'] = medicines_list
            return result
        except Exception as e:
            logging.error(f"获取处方详情失败: {str(e)}")
            api.abort(500, f"获取处方详情失败: {str(e)}")
    
    @api.doc('更新处方')
    @api.expect(prescription_model)
    @jwt_required()
    def put(self, prescription_id):
        """更新处方信息"""
        prescription = Prescription.query.get_or_404(prescription_id)
        data = request.json
        
        prescription.instructions = data.get('instructions', prescription.instructions)
        prescription.status = data.get('status', prescription.status)
        
        # 更新处方明细 - 先删除旧的
        PrescriptionDetail.query.filter_by(prescription_id=prescription.prescription_id).delete()
        
        # 添加新的处方明细
        if 'medicines' in data:
            for med in data['medicines']:
                detail = PrescriptionDetail(
                    prescription_id=prescription.prescription_id,
                    medicine_id=med['medicineId'],
                    quantity=med['quantity'],
                    instructions=med.get('usage', '')
                )
                db.session.add(detail)
        
        db.session.commit()
        
        # 返回更新后的完整处方信息
        updated_prescription = prescription.to_dict()
        details = PrescriptionDetail.query.filter_by(prescription_id=prescription.prescription_id).all()
        medicines_list = []
        
        for detail in details:
            medicine = Medicine.query.get(detail.medicine_id)
            if medicine:
                med_dict = medicine.to_dict()
                med_dict['quantity'] = detail.quantity
                med_dict['usage'] = detail.instructions
                medicines_list.append(med_dict)
        
        updated_prescription['medicines'] = medicines_list
        return updated_prescription
