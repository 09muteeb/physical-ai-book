import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
          <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
          <div className="text--center padding-horiz--md">
            <p className={styles.descriptionText}>
              <strong>Physical AI</strong> bridges the gap between artificial intelligence and robotics,
              teaching you how to connect AI logic with physical robot bodies. This comprehensive guide
              covers ROS 2 as the robotic nervous system, digital twins and simulation for safe AI development,
              and NVIDIA Isaac for AI-powered robot brains.
            </p>
            <p className={styles.descriptionText}>
              Perfect for robotics enthusiasts, AI researchers, and developers looking to build intelligent
              systems that can interact with the real world through practical examples and theoretical foundations.
            </p>
          </div>
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

function BookDescription() {
  return (
    <section className={styles.bookDescriptionSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2 className={styles.bookDescriptionTitle}>About This Book</h2>
            <div className={styles.bookDescriptionContent}>
              <p className={`${styles.bookDescriptionText} ${styles.lead}`}>
                <strong>Physical AI</strong> is a comprehensive guide that bridges the gap between artificial intelligence and robotics.
                This book explores how to connect AI logic with physical robot bodies, creating intelligent systems that can interact with the real world.
              </p>
              <p className={styles.bookDescriptionText}>
                The book covers three essential modules:
                <strong> ROS 2 as the robotic nervous system</strong>,
                <strong> digital twins and simulation for safe AI development</strong>, and
                <strong> NVIDIA Isaac for AI-powered robot brains</strong>.
                Each module builds upon the previous to create a complete understanding of Physical AI.
              </p>
              <p className={styles.bookDescriptionText}>
                Whether you're a robotics enthusiast, AI researcher, or developer, this book provides
                practical examples and theoretical foundations to help you build AI agents that can
                effectively bridge to robot control systems and operate in the physical world.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
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
        <BookDescription />
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