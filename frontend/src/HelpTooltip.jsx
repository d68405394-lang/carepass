import React, { useState } from 'react';

const HelpTooltip = ({ title, content, videoUrl }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{ display: 'inline-block', position: 'relative', marginLeft: '8px' }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        onMouseEnter={() => setIsOpen(true)}
        onMouseLeave={() => setIsOpen(false)}
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          border: 'none',
          borderRadius: '50%',
          width: '24px',
          height: '24px',
          fontSize: '14px',
          fontWeight: 'bold',
          cursor: 'pointer',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
          transition: 'transform 0.2s ease',
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
        }}
      >
        ?
      </button>
      
      {isOpen && (
        <div
          style={{
            position: 'absolute',
            top: '30px',
            left: '0',
            zIndex: 1000,
            background: 'white',
            border: '2px solid #667eea',
            borderRadius: '8px',
            padding: '15px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            minWidth: '300px',
            maxWidth: '400px',
            animation: 'fadeIn 0.3s ease',
          }}
          onMouseEnter={() => setIsOpen(true)}
          onMouseLeave={() => setIsOpen(false)}
        >
          <h4 style={{ margin: '0 0 10px 0', color: '#667eea', fontSize: '16px' }}>
            💡 {title}
          </h4>
          <p style={{ margin: '0 0 10px 0', fontSize: '14px', lineHeight: '1.6', color: '#333' }}>
            {content}
          </p>
          {videoUrl && (
            <a
              href={videoUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                background: '#667eea',
                color: 'white',
                textDecoration: 'none',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: 'bold',
                transition: 'background 0.3s ease',
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = '#5568d3';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = '#667eea';
              }}
            >
              📹 チュートリアル動画を見る
            </a>
          )}
        </div>
      )}
      
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default HelpTooltip;
