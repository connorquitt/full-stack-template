import React from 'react';
import { NavLink } from 'react-router-dom';
import '../index.css';

function NavBar() {
    return (
        <nav className='navbar'>
            <NavLink to='/example'>example</NavLink>
        </nav>
    )
}

export default NavBar;