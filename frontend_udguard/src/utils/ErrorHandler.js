import Swal from 'sweetalert2'

export const handleApiError = (error) => {
  Swal.fire({
    title: 'Error',
    text: error.response?.data?.message || 'Ha ocurrido un error',
    icon: 'error',
    confirmButtonText: 'OK'
  })
}
