import React, { useState, useEffect } from 'react';
import { Button } from './Button';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const [click, setClick] = useState(false);
  const [button, setButton] = useState(true);
  const [showAuthForm, setShowAuthForm] = useState(false);

  const handleClick = () => setClick(!click);
  const closeMobileMenu = () => setClick(false);

  const showButton = () => {
    if (window.innerWidth <= 960) {
      setButton(false);
    } else {
      setButton(true);
    }
  };

  const toggleAuthForm = () => setShowAuthForm(!showAuthForm);
  const closeAuthForm = () => setShowAuthForm(false);

  useEffect(() => {
    showButton();
  }, []);

  window.addEventListener('resize', showButton);

  const submitAuthForm = (event) => {
    event.preventDefault();
    // Add form submission logic here
    closeAuthForm();
  };

  return (
    <>
      <nav className='navbar'>
        <div className='navbar-container'>
          <Link to='/' className='navbar-logo' onClick={closeMobileMenu}>
            InnerVoice - AI
            <i className='fab fa-typo3' />
          </Link>
          <div className='menu-icon' onClick={handleClick}>
            <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
          </div>
          <ul className={click ? 'nav-menu active' : 'nav-menu'}>
          </ul>
          {button && <Button buttonStyle='btn--outline' onClick={toggleAuthForm}>SIGN UP</Button>}
        </div>
      </nav>
      {showAuthForm && (
        <div id="authForm" className="auth-form">
          <form id="authFormContent" onSubmit={submitAuthForm}>
            <label id="authFormTitle">Sign In</label><br />
            <input type="text" id="username" name="username" placeholder="Username" required /><br /><br />
            <input type="password" id="password" name="password" placeholder="Password" required /><br /><br />
            <input type="text" id="preferredName" name="preferredName" placeholder="Preferred Name" required /><br /><br />
            <button type="submit" id="submitBtn">Submit</button>
            <button type="button" onClick={closeAuthForm}>Cancel</button>
          </form>
        </div>
      )}
    </>
  );
}

export default Navbar;
