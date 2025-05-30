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
    # @jwt_required()
    def get(self, medicine_id):
        """获取药品详情"""
        medicine = Medicine.query.get_or_404(medicine_id)
        return medicine.to_dict()

@api.route('')
class PrescriptionList(Resource):
    @api.doc('创建处方')
    @api.expect(prescription_model)
    def post(self):
        """创建新处方"""
        data = request.json
        print(f"创建处方: {data}")
        try:
        
            prescription = Prescription(
                patient_id=data['patientId'],
                doctor_id=data['doctorId'],
                instructions=data.get('instructions', ''),
                status=data.get('status', 'pending')
            )
            
            db.session.add(prescription)
            db.session.flush()  # 获取新处方ID
        except Exception as e:
            #如果是外键约束错误，回滚
            db.session.rollback()
            logging.error(f"创建处方失败: {str(e)}")
            api.abort(400, f"创建处方失败: {str(e)}")
        
        # 添加处方明细
        for med in data['medicines']:
            detail = PrescriptionDetail(
                prescription_id=prescription.prescription_id,
                medicine_id=med['id'],
                quantity=med['quantity'],
                instructions=med.get('usage', '')
            )
            db.session.add(detail)
        
        # 在提交前保存必要的数据
        prescription_id = prescription.prescription_id
        patient_id = prescription.patient_id
        doctor_id = prescription.doctor_id
        created_at = prescription.created_at
        instructions = prescription.instructions
        status = prescription.status
        
        db.session.commit()
        
        # 构建返回结果
        result = {
            'id': prescription_id,
            'patientId': patient_id,
            'doctorId': doctor_id,
            'date': created_at.isoformat() if created_at else None,
            'instructions': instructions,
            'status': status,
            'medicines': []
        }
        
        # 补充药品信息
        details = PrescriptionDetail.query.filter_by(prescription_id=prescription_id).all()
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
        
        # 现在可以安全地移除会话
        db.session.remove()
        
        return result, 201

    @api.doc('获取处方列表')
    @api.param('id', '医生或者患者ID')
    @api.param('type', '类型 (doctor/patient)')
    def get(self):
        """获取处方列表，可按 id 过滤"""
        type = request.args.get('type')
        id = request.args.get('id')
        print(f"获取处方列表，类型: {type}, ID: {id}")
        query = Prescription.query
        
        if type == 'patient' and id:
            query = query.filter_by(patient_id=id)
        elif type == 'doctor' and id:
            query = query.filter_by(doctor_id=id)
        
        prescriptions = query.all()
        print(f"查询到 {len(prescriptions)} 条处方记录")
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
        print(f"返回 {len(result)} 条处方记录")
        
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
