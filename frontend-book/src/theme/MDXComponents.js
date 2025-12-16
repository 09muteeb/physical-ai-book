import React from 'react';
import {useThemeConfig} from '@docusaurus/theme-common';
import Heading from '@theme/Heading';
import Details from '@theme/Details';
import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

// Custom components for enhanced UI
const Card = ({children, title, icon, className = ''}) => (
  <div className={`card-custom ${className}`}>
    {(title || icon) && (
      <div className="card-header">
        {icon && <span className="card-icon">{icon}</span>}
        {title && <h3 className="card-title">{title}</h3>}
      </div>
    )}
    <div className="card-body">{children}</div>
  </div>
);

const Badge = ({children, type = 'default', className = ''}) => (
  <span className={`badge badge--${type} ${className}`}>{children}</span>
);

const Alert = ({children, type = 'info', className = ''}) => (
  <div className={`alert alert--${type} ${className}`}>
    <div className="alert-content">{children}</div>
  </div>
);

const Button = ({children, variant = 'primary', href, onClick, className = '', size = 'normal'}) => {
  const classes = `button button--${variant} button--${size} ${className}`;

  if (href) {
    return (
      <a href={href} className={classes} onClick={onClick}>
        {children}
      </a>
    );
  }

  return (
    <button className={classes} onClick={onClick}>
      {children}
    </button>
  );
};

// Enhanced MDX Components
export default {
  h1: (props) => <Heading as="h1" {...props} />,
  h2: (props) => <Heading as="h2" {...props} />,
  h3: (props) => <Heading as="h3" {...props} />,
  h4: (props) => <Heading as="h4" {...props} />,
  h5: (props) => <Heading as="h5" {...props} />,
  h6: (props) => <Heading as="h6" {...props} />,
  details: Details,
  tabItem: TabItem,
  tabs: Tabs,
  // Custom components
  Card,
  Badge,
  Alert,
  Button,
};