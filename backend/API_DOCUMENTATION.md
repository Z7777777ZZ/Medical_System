# Medical System API Documentation

## Database Changes

### Existing Tables
The following tables are from the original development manual:
- patients
- hospitals
- departments
- doctors
- patient_details
- medicines
- prescriptions
- prescription_details
- medical_records
- appointments
- payments

### New/Modified Tables
1. **queues** (Modified)
   - Added `priority` field (BOOLEAN) to support priority queue
   - Added `created_at` and `updated_at` timestamps
   - Modified `status` enum to only include 'waiting' and 'called'

## API Endpoints

### Queue Management

#### Get Doctor's Queue
```
GET /api/queue/doctor/<doctor_id>
```
Returns the current queue for a specific doctor, ordered by queue number.

Response:
```json
[
    {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "queue_number": 1,
        "status": "waiting",
        "priority": false,
        "created_at": "2023-04-21T10:00:00",
        "updated_at": "2023-04-21T10:00:00"
    }
]
```

#### Get Patient's Queue Status
```
GET /api/queue/patient/<patient_id>
```
Returns the current queue status for a specific patient.

Response:
```json
{
    "id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "queue_number": 1,
    "status": "waiting",
    "priority": false,
    "created_at": "2023-04-21T10:00:00",
    "updated_at": "2023-04-21T10:00:00"
}
```

#### Join Queue
```
POST /api/queue/join
```
Adds a patient to the queue.

Request Body:
```json
{
    "patient_id": 1,
    "doctor_id": 1,
    "priority": false
}
```

Response:
```json
{
    "id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "queue_number": 1,
    "status": "waiting",
    "priority": false,
    "created_at": "2023-04-21T10:00:00",
    "updated_at": "2023-04-21T10:00:00"
}
```

#### Call Next Patient
```
POST /api/queue/call-next
```
Calls the next patient in the queue, prioritizing patients with priority status.

Request Body:
```json
{
    "doctor_id": 1
}
```

Response:
```json
{
    "id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "queue_number": 1,
    "status": "called",
    "priority": false,
    "created_at": "2023-04-21T10:00:00",
    "updated_at": "2023-04-21T10:00:00"
}
```

#### Finish Diagnosis
```
POST /api/queue/finish/<queue_id>
```
Removes a patient from the queue after diagnosis is complete.

Response:
```json
{
    "message": "Diagnosis finished"
}
```

## Frontend Integration

To integrate with the frontend, replace the static data in the following files with API calls:

1. `src/stores/queueStore.js`:
   - Replace static queue data with API calls to `/api/queue/doctor/<doctor_id>`
   - Replace `callNextPatient` with POST to `/api/queue/call-next`
   - Replace `returnToQueueAfterExam` with POST to `/api/queue/join` with priority=true
   - Replace `finishDiagnosis` with POST to `/api/queue/finish/<queue_id>`

2. `src/views/patient/Queue.vue`:
   - Replace static queue data with API call to `/api/queue/patient/<patient_id>`
   - Replace `submitRegister` with POST to `/api/queue/join`

## Authentication

All API endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

Error responses include a message:
```json
{
    "message": "Error description"
}
``` 