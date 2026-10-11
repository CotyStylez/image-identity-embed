# IdentityEmbed — Cryptographic Image Signer & Verifier with Cash App Modal

Make IdentityEmbed a production-ready, fully functional client-side cryptographic image provenance suite that supports real Ed25519/WebCrypto signing, binary EXIF metadata embedding, real-time image authenticity verification, and a modern Cash App ($static9072) donation modal.

## User Review & Critical Decisions

> [!IMPORTANT]
> The following user preferences were confirmed in Phase 1 clarification:
> - **Payment Service**: Keep Cash App ($static9072) with a modern interactive modal featuring quick amount presets ($1, $5, $10), one-click Cashtag copying, and direct deep-linking.
> - **Core Cryptographic Scope**: Provide both cryptographic **Signing & EXIF Embedding** and an on-page **Provenance Verification** tool to validate signed images against image tampering.
> - **Processing Model**: Pure client-side execution in the browser for privacy and security—no private keys or images uploaded to external servers.

---

## 1. Overview & Core Concept

- **What It Does**: A standalone browser-based cryptographic provenance workbench. Creators generate or import cryptographic keypairs, sign their source images with SHA-256 + digital signatures, embed the structured provenance record into the image EXIF/metadata, and export the authenticated file. Any recipient or marketplace can drop an image into the Verifier tab to test cryptographic validity, view creator identity, and detect tampering.
- **Target Audience / Persona**: Digital artists, photographers, journalists, NFT/creative creators, and provenance researchers who need verifiable proof of authorship without vendor lock-in or SaaS subscriptions.
- **Key Value**: Real mathematical proof of creation and image integrity that travels inside the image file itself, paired with a seamless tip/support flow via Cash App.

---

## 2. User Experience & Visual Design

### Key User Flows
1. **Mode Switching**: The main interface presents a clean segmented tab bar: **Sign & Protect** and **Verify Authenticity**.
2. **Signing Flow**:
   - Creator enters identity (e.g. name, social handle, email).
   - Generates an Ed25519/WebCrypto keypair with one click, or pastes an existing PEM/raw key.
   - Uploads an image (JPEG, PNG, WEBP).
   - Clicks **"Embed Signature & Metadata"**: The app calculates the image SHA-256 digest, cryptographically signs the combined payload, injects the provenance dictionary into the image's EXIF UserComment structure, and provides a direct download of the signed image.
   - Shows interactive metadata inspector and public key fingerprint for record-keeping.
3. **Verification Flow**:
   - User drops any signed image file into the dropzone.
   - The app reads binary EXIF metadata, extracts the embedded provenance payload and digital signature.
   - Recomputes the SHA-256 hash of the image pixel/data content.
   - Performs cryptographic signature verification against the embedded or provided public key.
   - Renders a conclusive verification banner: Authenticity Verified (Green) with creator details & timestamp, Tampered / Invalid (Red), or No Signature Detected (Neutral).
4. **Cash App Support Modal**:
   - Top bar and footer feature a sleek "Support Creator" Cash App button with a distinctive emerald accent.
   - Clicking opens an interactive modal:
     - Profile display: `$static9072` with Cash App badge.
     - Presets: $1, $5, $10, and custom amount.
     - Direct button opening `https://cash.app/$static9072/[amount]` in a safe target window.
     - Copy Cashtag button with instantaneous clipboard feedback.
     - Cash App mobile QR code for instant smartphone scanning.

### Visual Identity & Theme
- **Aesthetic**: Technical studio dashboard with dark theme (`#0F172A` neutral canvas, `#1E293B` structural cards, `#6366F1` indigo action accents, `#10B981` emerald verification & Cash App accents).
- **Typography**: Clean display hierarchy (`Plus Jakarta Sans` or modern sans), paired with `font-mono tabular-nums` for cryptographic hashes, signatures, public keys, and timestamps.
- **Component Styling**: Strict zero-pill discipline for static metadata; single-elevation depth; explicit state feedback on drag-over, signing, and verification.

---

## 3. Key Product Decisions & Trade-Offs

- **Pure Client-Side Cryptography & EXIF Processing**:
  - *Chosen Approach*: Leverage standard Web Crypto API (`window.crypto.subtle`) for hashing and digital signatures, alongside client-side EXIF binary manipulation (via piexifjs/binary parser).
  - *Why*: Absolute privacy guarantee—neither private keys nor proprietary image artwork leave the user's browser.
  - *Alternatives Considered*: Server-side Node.js processing was rejected by user choice in Phase 1 to guarantee zero data leakage.
- **Cash App Modal with QR & Deep Links**:
  - *Chosen Approach*: An interactive modal combining deep links, instant copy feedback, and visual QR code presentation.
  - *Why*: Many desktop users donate via their phone by scanning a QR code or copying the tag into their mobile app, while mobile users benefit from direct URL navigation.

---

## 4. Technical Architecture & Data Strategy

```
┌────────────────────────────────────────────────────────────────────────┐
│                        IdentityEmbed Studio                            │
├────────────────────────────────────────────────────────────────────────┤
│  Top Navigation (Brand Wordmark, Mode Switcher, Cash App Support CTA)  │
├──────────────────────────────────┬─────────────────────────────────────┤
│          SIGN & EMBED            │         VERIFY PROVENANCE           │
│  - Creator identity input        │  - Image dropzone & file reader     │
│  - Ed25519/WebCrypto key manager │  - Binary EXIF parser (UserComment) │
│  - Image canvas & SHA-256 hasher │  - Image hash recalculation         │
│  - Digital signature generator   │  - Cryptographic signature verifier │
│  - EXIF UserComment injector     │  - Authenticity report card         │
│  - Signed image blob downloader  │  - Tamper detection diagnostics     │
├──────────────────────────────────┴─────────────────────────────────────┤
│  Cash App Modal: $static9072 / QR Code / Quick Presets ($1, $5, $10)   │
└────────────────────────────────────────────────────────────────────────┘
```

### Data Model & State
- **Keypair State**: `{ privateKeyPem, publicKeyPem, keyId, algorithm }`
- **Provenance Payload**:
  ```json
  {
    "identityEmbed": {
      "version": "1.0",
      "creator": "Creator Name",
      "timestamp": "2026-10-11T17:45:00.000Z",
      "imageHash": "sha256-abcdef123...",
      "publicKey": "...",
      "signature": "..."
    }
  }
  ```
- **Verification State**: `{ status: 'idle' | 'valid' | 'tampered' | 'unsigned', creator, timestamp, expectedHash, actualHash, keyId }`
