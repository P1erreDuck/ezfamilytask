import { defineStore } from 'pinia'

export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),

  actions: {
    async addItem(text) {
      this.loading = true
      this.error = null

      try {
        const res = await fetch('http://localhost:8000/api/items/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        })

        if (!res.ok) {
          const error = await res.json()
          throw new Error(error.detail || 'Ошибка добавления')
        }

        const newItem = await res.json()
        this.items.unshift(newItem)

      } catch (e) {
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    },

    async updateItem(id, newText) {
      this.loading = true
      this.error = null

      try {
        const res = await fetch(`http://localhost:8000/api/items/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: newText })
        })

        if (!res.ok) {
          const error = await res.json()
          throw new Error(error.detail || 'Ошибка обновления')
        }

        const updatedItem = await res.json()
        const index = this.items.findIndex(item => item.id === id)
        if (index !== -1) {
          this.items[index] = updatedItem
        }

      } catch (e) {
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    },

    async fetchItems(limit = 20) {
      this.loading = true
      this.error = null

      try {
        const res = await fetch(
          `http://localhost:8000/api/items/?limit=${limit}`
        )

        if (!res.ok) {
          throw new Error('Ошибка загрузки')
        }

        this.items = await res.json()

      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },

    async deleteItem(id) {
      this.loading = true
      this.error = null

      try {
        const res = await fetch(`http://localhost:8000/api/items/${id}`, {
          method: 'DELETE'
        })

        if (!res.ok && res.status !== 204) {
          throw new Error('Ошибка удаления')
        }

        this.items = this.items.filter(item => item.id !== id)

      } catch (e) {
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    }
  }
})