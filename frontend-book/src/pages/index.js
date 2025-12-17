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
        <div className={styles.heroContent}>
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.authorSection}>
            <div className={styles.profileContainer}>
              <img
                src="/img/My-pic.jpeg"
                alt="Ali Hyder"
                className={styles.profilePic}
                onClick={() => {
                  const modal = document.createElement('div');
                  modal.style.position = 'fixed';
                  modal.style.top = '0';
                  modal.style.left = '0';
                  modal.style.width = '100%';
                  modal.style.height = '100%';
                  modal.style.backgroundColor = 'rgba(0,0,0,0.9)';
                  modal.style.display = 'flex';
                  modal.style.justifyContent = 'center';
                  modal.style.alignItems = 'center';
                  modal.style.zIndex = '9999';
                  modal.style.cursor = 'pointer';

                  const img = document.createElement('img');
                  img.src = '/img/My-pic.jpeg';
                  img.alt = 'Ali Hyder';
                  img.style.maxWidth = '90%';
                  img.style.maxHeight = '90%';
                  img.style.objectFit = 'contain';

                  modal.appendChild(img);
                  document.body.appendChild(modal);

                  modal.addEventListener('click', () => {
                    document.body.removeChild(modal);
                  });
                }}
              />
            </div>
            <p className={styles.authorLine}>Made by <strong>Ali Hyder</strong> - The Author</p>
          </div>
        </div>
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
        {/* Images Section */}
        <section className={styles.imagesSection}>
          <div className="container">
            <div className="row">
              <div className={`col col--4 ${styles.col} ${styles.responsiveCol}`} style={{padding: '10px'}}>
                <img
                  src="/img/pic-1.png"
                  alt="Physical AI"
                  style={{width: '100%', height: 'auto', borderRadius: '8px'}}
                />
                <h2 className={styles.imageTitle}>Physical AI</h2>
                <p className={styles.imageDescription}>Learn how to connect artificial intelligence with the physical world through robotics.</p>
              </div>
              <div className={`col col--4 ${styles.col} ${styles.responsiveCol}`} style={{padding: '10px'}}>
                <img
                  src="/img/pic-2.png"
                  alt="ROS 2 Fundamentals"
                  style={{width: '100%', height: 'auto', borderRadius: '8px'}}
                />
                <h2 className={styles.imageTitle}>ROS 2 Fundamentals</h2>
                <p className={styles.imageDescription}>Understand how ROS 2 serves as the "nervous system" connecting AI to robot bodies.</p>
              </div>
              <div className={`col col--4 ${styles.col} ${styles.responsiveCol}`} style={{padding: '10px'}}>
                <img
                  src="/img/pic-3.png"
                  alt="Practical Examples"
                  style={{width: '100%', height: 'auto', borderRadius: '8px'}}
                />
                <h2 className={styles.imageTitle}>Practical Examples</h2>
                <p className={styles.imageDescription}>Real-world examples of AI agents bridging to robot control systems.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}