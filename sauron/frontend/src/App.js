import logo from './logo.svg';
import './App.css';
import Topbar from './Components/Topbar/Topbar';
import Packageinfo from './Components/Info/PackageInfo';
import PackageStats from './Components/Stats/PackageStats';
import Community from './Components/Community/Community';
import Home from './Components/Home/Home'

function App() {
  return (
    <div className="App">
      <Topbar></Topbar>
      <Home></Home>
      {/* <Topbar></Topbar>
      <Packageinfo></Packageinfo>
      <PackageStats></PackageStats>
      <Community></Community> */}
    </div>
  );
}

export default App;
