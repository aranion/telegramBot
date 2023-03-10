import { initializeApp } from 'firebase/app'
import type { FirebaseApp } from 'firebase/app'
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'
import { Database as DatabaseType, getDatabase, ref, set } from 'firebase/database'
import { config } from '../config'

class Database {
  app: FirebaseApp | null = null
  db: DatabaseType | null = null

  constructor() {
    try {
      this.app = initializeApp({ ...config.firebase })

      const auth = getAuth()
      const { email, password } = config.authorFirebase

      signInWithEmailAndPassword(auth, email, password).catch(err => {
        console.error(err)
      })

      this.db = getDatabase(this.app)
    } catch (error) {
      console.error('Ошибка инициализации database')
      console.error(error)
    }
  }

  writeMessage(message: string, time: number): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.db) {
        set(ref(this.db, 'messages/' + time), {
          message,
        })
          .then(resolve, reject)
          .catch(reject)
      }
    })
  }
}

const db = new Database()

export default db
