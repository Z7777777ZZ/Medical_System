import axios from 'axios'

const service = axios.create({
  baseURL: 'http://127.0.0.1:5000'
  // baseURL: 'http://172.29.101.55:5000'
})

export default service