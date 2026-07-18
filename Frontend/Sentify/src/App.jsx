import { useState } from 'react'
import SideBar from './components/SideBar'
import MainChat from './components/DisplayComponents/MainChat'
import Instruction from './components/DisplayComponents/Instruction'

function App() {
  const [activePage, setActivePage] = useState('chat')

  const renderPage = () => {
    switch (activePage) {
      case 'chat':        return <MainChat />
      case 'instruction': return <Instruction />
      default:            return <MainChat />
    }
  }

  return (
    <div className="flex h-screen overflow-hidden bg-white">
      <SideBar activePage={activePage} onNavigate={setActivePage} />
      <main className="flex-1 overflow-y-auto">
        <div className="min-h-full flex flex-col justify-center items-center p-6">
          {renderPage()}
        </div>
      </main>
    </div>
  )
}

export default App
