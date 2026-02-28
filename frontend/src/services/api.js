import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export const fetchRoute = async (route) => {
  const response = await api.get('/strava/route', {
    params: { route }
  })
  return response.data
}
