import React from 'react'
import logo from '../Topbar/logo.png'
import './home.css'
function Home() {
    return (
        <div className='home'>
            <img src={logo}></img>
            <h1>Sauron - OSS Security inspector</h1>
            <h4>One tool to rule them all, one tool to find them, One tool to bring them all, and in the darkness bind them.</h4>
        </div>
    )
}

export default Home
