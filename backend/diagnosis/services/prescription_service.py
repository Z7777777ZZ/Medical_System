from app import db
from diagnosis.models.prescription import Prescription, PrescriptionDetail, Medicine
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
import logging

class PrescriptionService:
    @staticmethod
    def get_medicines():
        """获取所有药品列表"""
        try:
            medicines = Medicine.query.all()
            return [medicine.to_dict() for medicine in medicines]
        except Exception as e:
            logging.error(f"获取药品列表失败: {str(e)}")
            return []
    
    @staticmethod
    def get_medicine(medicine_id):
        """根据ID获取药品"""
        try:
            medicine = Medicine.query.get(medicine_id)
            return medicine.to_dict() if medicine else None
        except Exception as e:
            logging.error(f"获取药品失败: {str(e)}")
            return None
    
    @staticmethod
    def create_prescription(data):
        """创建处方"""
        try:
            # 创建处方记录
            prescription = Prescription(
                patient_id=data.get('patientId'),
                doctor_id=data.get('doctorId', 1),  # 默认为当前医生
                diagnosis=data.get('diagnosis', '')
            )
            
            db.session.add(prescription)
            db.session.flush()  # 获取新生成的ID
            
            # 添加处方明细
            if 'medicines' in data and isinstance(data['medicines'], list):
                for med_data in data['medicines']:
                    detail = PrescriptionDetail(
                        prescription_id=prescription.prescription_id,
                        medicine_id=med_data.get('medicineId'),
                        dosage=med_data.get('dosage', ''),
                        frequency=med_data.get('frequency', ''),
                        duration=med_data.get('duration', ''),
                        instructions=med_data.get('instructions', '')
                    )
                    db.session.add(detail)
            
            db.session.commit()
            return prescription.to_dict()
        
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"创建处方失败: {str(e)}")
            return None
    
    @staticmethod
    def get_prescription(prescription_id):
        """获取处方详情"""
        try:
            prescription = Prescription.query.get(prescription_id)
            return prescription.to_dict() if prescription else None
        except Exception as e:
            logging.error(f"获取处方失败: {str(e)}")
            return None
    
    @staticmethod
    def get_patient_prescriptions(patient_id):
        """获取患者的处方列表"""
        try:
            prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
            return [p.to_dict() for p in prescriptions]
        except Exception as e:
            logging.error(f"获取患者处方失败: {str(e)}")
            return []
    
    @staticmethod
    def update_prescription(prescription_id, data):
        """更新处方"""
        try:
            prescription = Prescription.query.get(prescription_id)
            if not prescription:
                return None
            
            # 更新处方基本信息
            if 'diagnosis' in data:
                prescription.diagnosis = data['diagnosis']
            
            if 'status' in data:
                prescription.status = data['status']
            
            # 如果提供了新的药品列表，先删除旧的明细
            if 'medicines' in data and isinstance(data['medicines'], list):
                # 删除现有明细
                PrescriptionDetail.query.filter_by(prescription_id=prescription_id).delete()
                
                # 添加新明细
                for med_data in data['medicines']:
                    detail = PrescriptionDetail(
                        prescription_id=prescription_id,
                        medicine_id=med_data.get('medicineId'),
                        dosage=med_data.get('dosage', ''),
                        frequency=med_data.get('frequency', ''),
                        duration=med_data.get('duration', ''),
                        instructions=med_data.get('instructions', '')
                    )
                    db.session.add(detail)
            
            db.session.commit()
            return prescription.to_dict()
        
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"更新处方失败: {str(e)}")
            return None
