from app import db
from diagnosis.models.prescription import Prescription, PrescriptionDetail, Medicine
from datetime import datetime

class PrescriptionService:
    @staticmethod
    def create_prescription(data):
        """创建新处方"""
        prescription = Prescription(
            patientId=data['patientId'],
            doctorId=data['doctorId'],
            date=datetime.now(),
            instructions=data.get('instructions', ''),
            status='draft'
        )
        db.session.add(prescription)
        db.session.flush()  # 获取 prescription_id

        # 添加处方明细
        for medicine in data['medicines']:
            detail = PrescriptionDetail(
                prescriptionId=prescription.id,
                medicineId=medicine['id'],
                quantity=medicine['quantity'],
                instructions=medicine['usage']
            )
            db.session.add(detail)

        db.session.commit()
        return prescription.to_dict()

    @staticmethod
    def get_prescription(prescription_id):
        """获取处方详情"""
        prescription = Prescription.query.get(prescription_id)
        if not prescription:
            return None
        return prescription.to_dict()

    @staticmethod
    def get_patient_prescriptions(patient_id):
        """获取患者的所有处方"""
        prescriptions = Prescription.query.filter_by(patientId=patient_id).all()
        return [p.to_dict() for p in prescriptions]

    @staticmethod
    def get_doctor_prescriptions(doctor_id):
        """获取医生的所有处方"""
        prescriptions = Prescription.query.filter_by(doctorId=doctor_id).all()
        return [p.to_dict() for p in prescriptions]

    @staticmethod
    def get_available_medicines():
        """获取可用药品列表"""
        medicines = Medicine.query.all()
        return [m.to_dict() for m in medicines]

    @staticmethod
    def update_prescription(prescription_id, data):
        """更新处方信息"""
        prescription = Prescription.query.get(prescription_id)
        if not prescription:
            return None

        # 更新基本信息
        if 'instructions' in data:
            prescription.instructions = data['instructions']
        if 'status' in data:
            prescription.status = data['status']

        # 更新药品明细
        if 'medicines' in data:
            # 删除旧的明细
            PrescriptionDetail.query.filter_by(prescriptionId=prescription_id).delete()
            
            # 添加新的明细
            for medicine in data['medicines']:
                detail = PrescriptionDetail(
                    prescriptionId=prescription_id,
                    medicineId=medicine['id'],
                    quantity=medicine['quantity'],
                    instructions=medicine['usage']
                )
                db.session.add(detail)

        db.session.commit()
        return prescription.to_dict()

    @staticmethod
    def check_medicine_conflicts(medicines):
        """检查药品冲突（示例实现）"""
        # 这里可以实现药品冲突检测逻辑
        # 例如：检查是否有相互作用的药品组合
        return []

    @staticmethod
    def calculate_dosage(medicine_id, patient_weight, patient_age):
        """计算药品剂量（示例实现）"""
        # 这里可以实现基于体重和年龄的剂量计算逻辑
        # 返回建议剂量
        return {
            'suggestedDosage': '1片',
            'frequency': '一日三次',
            'notes': '饭后服用'
        } 