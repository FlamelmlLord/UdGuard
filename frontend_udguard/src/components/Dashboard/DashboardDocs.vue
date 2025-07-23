<template>
  <div class="docs-page">
    <div class="documents-container">
      <h1 class="page-title">Gestor de Documentos</h1>

      <div class="documents-header">
        <div class="left-section">
          <div class="search-bar">
            <i class="mdi mdi-magnify search-icon"></i>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Buscar documento..."
              class="search-input"
            />
          </div>
        </div>
        <div class="header-buttons">
          <button
            v-if="selectedDocumentsCount >= 2"
            class="delete-selected-button"
            @click="confirmDeleteSelected"
          >
            <i class="mdi mdi-delete icon"></i>
            <span class="button-text">Eliminar Seleccionados ({{selectedDocumentsCount}})</span>
          </button>
          <button class="add-document-button" @click="openAddDocumentModal">
            <i class="mdi mdi-plus icon"></i>
            <span class="button-text">Añadir Documento</span>
          </button>
        </div>
      </div>

      <div class="documents-table">
        <div class="table-header">
          <div class="checkbox-column"></div>
          <div class="name-column">Nombre</div>
          <div class="date-column">Última Modificación</div>
          <div class="actions-column">Acciones</div>
        </div>

        <div class="table-body">
          <p v-if="filteredDocuments.length === 0" class="empty-table-message">
            No hay documentos disponibles.
          </p>
          <div
            v-for="document in paginatedDocuments"
            :key="document.id"
            :class="['table-row', { 'selected': document.selected }]"
            @click="toggleSelect(document)"
          >
            <div class="checkbox-column">
              <i v-if="document.selected" class="mdi mdi-check check-icon"></i>
            </div>
            <div class="name-column">
              <i class="mdi mdi-file-document-outline file-icon"></i>
              <span class="document-name">{{ document.name }}</span>
            </div>
            <div class="date-column">{{ document.modified }}</div>
            <div class="actions-column">
              <button class="action-button" @click.stop="downloadDocument(document)">
                <i class="mdi mdi-download action-icon"></i>
              </button>
              <button class="action-button" @click.stop="confirmDelete(document)">
                <i class="mdi mdi-delete action-icon"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="pagination" v-if="filteredDocuments.length > 10">
          <button
            class="pagination-button"
            @click="prevPage"
            :disabled="currentPage === 1"
          >
            <i class="mdi mdi-chevron-left"></i>
          </button>
          <span class="page-info">{{ currentPage }} de {{ totalPages }}</span>
          <button
            class="pagination-button"
            @click="nextPage"
            :disabled="currentPage === totalPages"
          >
            <i class="mdi mdi-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal para añadir documento -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2>Añadir Nuevo Documento</h2>
        <form @submit.prevent="addDocument" class="add-document-form">
          <div class="form-group">
            <label for="documentName">Nombre del documento</label>
            <input
              type="text"
              id="documentName"
              v-model="newDocument.name"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="documentFile">Archivo</label>
            <input
              type="file"
              id="documentFile"
              @change="handleFileUpload"
              required
              class="form-input"
            />
          </div>
          <div class="modal-actions">
            <button type="button" class="cancel-button" @click="closeModal">
              Cancelar
            </button>
            <button type="submit" class="submit-button">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardDocs',
  data () {
    return {
      documents: [],
      searchQuery: '',
      showModal: false,
      newDocument: {
        name: '',
        file: null
      },
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    filteredDocuments () {
      return this.documents.filter(doc =>
        doc.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    totalPages () {
      return Math.ceil(this.filteredDocuments.length / this.itemsPerPage)
    },
    paginatedDocuments () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredDocuments.slice(start, end)
    },
    selectedDocumentsCount () {
      return this.documents.filter(doc => doc.selected).length
    }
  },
  methods: {
    toggleSelect (document) {
      document.selected = !document.selected
    },
    prevPage () {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage () {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    openAddDocumentModal () {
      this.showModal = true
    },
    closeModal () {
      this.showModal = false
      this.newDocument = { name: '', file: null }
    },
    handleFileUpload (event) {
      this.newDocument.file = event.target.files[0]
    },
    async addDocument () {
      try {
        const newDoc = {
          id: Date.now(),
          name: this.newDocument.name,
          modified: new Date().toLocaleDateString(),
          file: this.newDocument.file,
          selected: false
        }
        this.documents.push(newDoc)
        this.closeModal()

        await this.$swal({
          icon: 'success',
          title: '¡Documento agregado!',
          text: 'El documento se ha agregado correctamente',
          confirmButtonColor: '#4CAF50'
        })
      } catch (error) {
        await this.$swal({
          icon: 'error',
          title: 'Error',
          text: 'No se pudo agregar el documento',
          confirmButtonColor: '#f44336'
        })
      }
    },
    downloadDocument (document) {
      console.log('Descargando documento:', document.name)
    },
    async confirmDelete (document) {
      const result = await this.$swal({
        title: '¿Estás seguro?',
        text: `¿Deseas eliminar el documento "${document.name}"?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#f44336',
        cancelButtonColor: '#999',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
      })

      if (result.isConfirmed) {
        this.deleteDocument(document)
      }
    },
    async confirmDeleteSelected () {
      const selectedDocs = this.documents.filter(doc => doc.selected)
      const result = await this.$swal({
        title: '¿Estás seguro?',
        text: `¿Deseas eliminar los ${selectedDocs.length} documentos seleccionados?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#f44336',
        cancelButtonColor: '#999',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
      })

      if (result.isConfirmed) {
        this.deleteSelectedDocuments()
      }
    },
    async deleteDocument (document) {
      this.documents = this.documents.filter(doc => doc.id !== document.id)

      await this.$swal({
        icon: 'success',
        title: '¡Eliminado!',
        text: 'El documento ha sido eliminado correctamente',
        confirmButtonColor: '#4CAF50'
      })
    },
    async deleteSelectedDocuments () {
      this.documents = this.documents.filter(doc => !doc.selected)

      await this.$swal({
        icon: 'success',
        title: '¡Eliminados!',
        text: 'Los documentos seleccionados han sido eliminados correctamente',
        confirmButtonColor: '#4CAF50'
      })
    }
  }
}
</script>
