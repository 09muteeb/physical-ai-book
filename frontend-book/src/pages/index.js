import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started - Read the Book
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Connecting AI Logic to Robot Bodies">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h2>Physical AI</h2>
                <p>Learn how to connect artificial intelligence with the physical world through robotics.</p>
              </div>
              <div className="col col--4">
                <h2>ROS 2 Fundamentals</h2>
                <p>Understand how ROS 2 serves as the "nervous system" connecting AI to robot bodies.</p>
              </div>
              <div className="col col--4">
                <h2>Practical Examples</h2>
                <p>Real-world examples of AI agents bridging to robot control systems.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}