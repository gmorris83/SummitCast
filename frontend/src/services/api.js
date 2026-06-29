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

export const addWeather = async (route, startTime) => {
  const response = await api.post('/weather', {
    route,
    start_time: startTime
  })
  return response.data
}
