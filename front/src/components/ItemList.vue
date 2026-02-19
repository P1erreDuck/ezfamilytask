<template>
  <div class="container">
    <h1>CRUD</h1>

    <div class="form">
      <input
        v-model="newItemText"
        type="text"
        placeholder="Введите имя"
        :class="{ 'error': textError }"
      />
      <button
        @click="addItem"
        :disabled="!newItemText.trim() || isAdding"
        class="action-btn add-btn"
      >
        {{ isAdding ? '...' : 'Добавить' }}
      </button>
      <p v-if="textError" class="error-text">{{ textError }}</p>
    </div>

    <div class="delete-form">
      <div class="delete-input-group">
        <input
          v-model="deleteId"
          type="text"
          placeholder="Удалить по ID"
          :class="{ 'error': deleteError }"
        />
        <button
          @click="confirmDelete"
          class="action-btn delete-id-btn"
          :disabled="!deleteId.trim()"
        >
          Удалить
        </button>
      </div>
      <p v-if="deleteError" class="error-text">{{ deleteError }}</p>
    </div>

    <div class="filter">
      <label>
        Показать:
        <input
          type="number"
          v-model.number="limit"
          min="1"
          max="100"
        />
        элементов
      </label>
      <button @click="loadItems" class="action-btn filter-btn">Обновить</button>
    </div>

    <div v-if="store.loading" class="loading">Загрузка...</div>
    <div v-else-if="store.items.length === 0" class="empty">Нет элементов</div>

    <ul v-else class="items-list">
      <li v-for="item in store.items" :key="item.id" class="item">
        <template v-if="editingId === item.id">
          <input
            v-model="editText"
            type="text"
            class="edit-input"
            @keyup.enter="saveEdit(item.id)"
            @keyup.esc="cancelEdit"
            ref="editInput"
          />
          <button @click="saveEdit(item.id)" class="icon-btn save-btn">✓</button>
          <button @click="cancelEdit" class="icon-btn cancel-btn">✗</button>
        </template>

        <template v-else>
          <span class="item-text">{{ item.text }}</span>
          <span class="item-id" @click="copyId(item.id)">
            {{ shortId(item.id) }}
            <span class="copy-hint" v-if="copiedId === item.id">Скопировано!</span>
          </span>
          <span class="item-date">{{ formatDate(item.created_at) }}</span>
          <div class="item-actions">
            <button @click="startEdit(item)" class="icon-btn edit-btn">✎</button>
            <button @click="deleteItem(item.id)" class="icon-btn delete-btn">×</button>
          </div>
        </template>
      </li>
    </ul>

    <div v-if="store.error" class="error-banner">{{ store.error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useItemsStore } from '../stores/items'

const store = useItemsStore()
const newItemText = ref('')
const textError = ref('')
const isAdding = ref(false)
const limit = ref(20)
const editingId = ref(null)
const editText = ref('')
const editInput = ref(null)
const deleteId = ref('')
const deleteError = ref('')
const copiedId = ref(null)

const addItem = async () => {
  if (!newItemText.value.trim()) return
  if (newItemText.value.length > 50) {
    textError.value = 'Превышен лимит'
    return
  }
  textError.value = ''
  isAdding.value = true
  try {
    await store.addItem(newItemText.value)
    newItemText.value = ''
  } finally {
    isAdding.value = false
  }
}

const startEdit = (item) => {
  editingId.value = item.id
  editText.value = item.text
  nextTick(() => editInput.value?.focus())
}

const saveEdit = async (id) => {
  if (!editText.value.trim()) return
  if (editText.value.length > 50) {
    store.error = 'Превышен лимит'
    return
  }
  try {
    await store.updateItem(id, editText.value)
    editingId.value = null
    editText.value = ''
  } catch {}
}

const cancelEdit = () => {
  editingId.value = null
  editText.value = ''
}

const deleteItem = async (id) => {
  if (confirm('Удалить элемент?')) {
    await store.deleteItem(id)
  }
}

const copyId = (id) => {
  navigator.clipboard.writeText(id)
  copiedId.value = id
  setTimeout(() => {
    copiedId.value = null
  }, 1500)
}

const confirmDelete = async () => {
  deleteError.value = ''
  if (!deleteId.value.trim()) {
    deleteError.value = 'Введите ID'
    return
  }
  const item = store.items.find(i => i.id === deleteId.value.trim())
  if (!item) {
    deleteError.value = 'ID не найден'
    return
  }
  if (confirm(`Удалить элемент "${item.text}"?`)) {
    await store.deleteItem(item.id)
    deleteId.value = ''
    deleteError.value = ''
  }
}

const loadItems = () => store.fetchItems(limit.value)

const shortId = (id) => {
  return id.substring(0, 8) + '...'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ru-RU', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

onMounted(loadItems)
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  margin-bottom: 30px;
}

.form, .delete-form {
  margin-bottom: 20px;
}

.form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.form input, .delete-input-group input {
  padding: 8px 12px;
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
  height: 36px;
  box-sizing: border-box;
}

.form input.error, .delete-input-group input.error {
  border-color: #ff4444;
}

.delete-input-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  height: 36px;
  width: 100px;
  box-sizing: border-box;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
}

.add-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.add-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.delete-id-btn {
  background-color: #d32f2f;
  color: white;
}

.delete-id-btn:hover:not(:disabled) {
  background-color: #b71c1c;
}

.delete-id-btn:disabled {
  background-color: #ffcdd2;
  cursor: not-allowed;
}

.error-text {
  color: #ff4444;
  font-size: 14px;
  margin-top: 5px;
  width: 100%;
}

.filter {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter label {
  display: flex;
  align-items: center;
  gap: 5px;
}

.filter input {
  width: 60px;
  padding: 4px;
}

.filter-btn {
  background-color: #2196F3;
  color: white;
  width: auto;
  min-width: 100px;
}

.filter-btn:hover {
  background-color: #1976D2;
}

.items-list {
  list-style: none;
  padding: 0;
}

.item {
  display: flex;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 4px;
  gap: 10px;
}

.item:hover {
  background-color: #f9f9f9;
}

.item-text {
  flex: 2;
}

.item-id {
  color: #999;
  font-size: 11px;
  font-family: monospace;
  background: #f0f0f0;
  padding: 4px 8px;
  border-radius: 3px;
  min-width: 90px;
  text-align: center;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s;
}

.item-id:hover {
  background-color: #e0e0e0;
}

.copy-hint {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  white-space: nowrap;
  animation: fadeInOut 1.5s;
  z-index: 10;
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}

.item-date {
  color: #999;
  font-size: 12px;
  min-width: 140px;
}

.item-actions {
  display: flex;
  gap: 5px;
  min-width: 69px;
  justify-content: flex-end;
}

.icon-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
}

.edit-btn:hover {
  background-color: #1976D2;
}

.delete-btn {
  background-color: #ff4444;
  color: white;
}

.delete-btn:hover {
  background-color: #cc0000;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
}

.save-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background-color: #5a6268;
}

.edit-input {
  flex: 1;
  padding: 6px;
  margin-right: 10px;
  border: 1px solid #4CAF50;
  border-radius: 4px;
  font-size: 14px;
  height: 32px;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.error-banner {
  margin-top: 20px;
  padding: 10px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  text-align: center;
}

@media (max-width: 600px) {
  .form {
    flex-direction: column;
    align-items: stretch;
  }
  .delete-input-group {
    flex-direction: column;
    align-items: stretch;
  }
  .action-btn {
    width: 100%;
  }
  .item {
    flex-wrap: wrap;
  }
}
</style>