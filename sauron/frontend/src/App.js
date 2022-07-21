import logo from './logo.svg';
import './App.css';
import Topbar from './Components/Topbar/Topbar';
import Packageinfo from './Components/Info/PackageInfo';
import PackageStats from './Components/Stats/PackageStats';
import Community from './Components/Community/Community';

function App() {
  return (
    <div className="App">
      <Topbar></Topbar>
      <Packageinfo></Packageinfo>
      <PackageStats></PackageStats>
      <Community></Community>
    </div>
  );
}

export default App;
