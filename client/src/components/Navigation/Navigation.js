import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GiHamburgerMenu } from "react-icons/gi";

import "./styles.css";

const Navigation = ({ updateUser }) => {
  const [menu, setMenu] = useState(false);

  const navigate = useNavigate();

  /* 
   Build a DELETE fetch request
    - On a successful delete clear the user from 
      state (updateUser is passed down from app via 
      props) and redirect back to the authentication route
      
    - Head back to server/app.py to build a route 
      that will keep our user logged in with sessions
  */
  const handleLogout = () => {
    fetch("/logout", { method: "DELETE" }).then((resp) => updateUser(null));
    navigate("/authentication");
  };

  const toggleMenu = () => setMenu((prev) => !prev);

  return (
    <div className="navigation">
      <h1 className="nav-title">Flatiron Theater Company</h1>
      <section className="nav-menu">
        {menu ? (
          <ul>
            <li className="close-button" onClick={() => setMenu(!menu)}>
              X
            </li>
            <li>
              <Link to="/productions/new">New Production</Link>
            </li>
            <li>
              <Link to="/"> Home</Link>
            </li>
            <li>
              <Link to="/authentication"> Login/Signup</Link>
            </li>
            <li className="logout-button" onClick={handleLogout}>
              {" "}
              Logout{" "}
            </li>
          </ul>
        ) : (
          <div className="hamburger-menu-wrapper" onClick={toggleMenu}>
            <GiHamburgerMenu size={30} />
          </div>
        )}
      </section>
    </div>
  );
};
export default Navigation;
