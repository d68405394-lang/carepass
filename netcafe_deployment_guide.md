# ネットカフェでのデプロイ手順書（GitHub + Render）

**作成日**: 2025年12月11日  
**作成者**: Manus AI

---

## 🎯 目的

この手順書は、ネットカフェなどの一時的な環境から、完成した「福祉事業所向け請求管理システム」を**Render**にデプロイするための詳細な手順を解説します。

## ⚠️ 注意事項

- **アカウント情報の管理**: ネットカフェのPCには、GitHubやRenderのパスワードを保存しないでください。作業終了後は必ずログアウトしてください。
- **ファイルの保存**: 作業ファイルはUSBメモリやクラウドストレージに保存し、PCを離れる際は必ず持ち帰ってください。
- **時間管理**: ネットカフェの利用時間には限りがあります。事前に全体の流れを把握し、計画的に作業を進めてください。

---

## 事前準備

### **必要なアカウント**

1. **GitHubアカウント**: コードを管理・公開するために必要です。
2. **Renderアカウント**: アプリケーションをデプロイするために必要です。

### **必要なファイル**

- **fukushi-system-final-ai-record.zip**: 最新のプロジェクトファイル

---

## 📚 デプロイ手順

### **ステップ1: GitHubリポジトリの作成とコードのプッシュ**

1. **GitHubにログイン**
   - ブラウザでGitHubにアクセスし、ログインします。

2. **新しいリポジトリを作成**
   - 「New repository」ボタンをクリックします。
   - **Repository name**: `fukushi-system`など、分かりやすい名前を入力します。
   - **Public**を選択します。（Renderの無料プランではPublicリポジトリが必要です）
   - 「Create repository」をクリックします。

3. **プロジェクトをアップロード**
   - `fukushi-system-final-ai-record.zip`を解凍します。
   - GitHubリポジトリのページで、「Add file」→「Upload files」を選択します。
   - 解凍したプロジェクトの**すべてのファイルとフォルダ**をドラッグ＆ドロップでアップロードします。
   - 「Commit changes」をクリックして、ファイルをリポジトリに保存します。

---

### **ステップ2: ReactプロジェクトのビルドとDjangoの設定**

このステップは、ローカル環境（サンドボックス）で実行済みの内容ですが、念のため確認します。

#### **2-1. Reactプロジェクトのビルド**

- `frontend`ディレクトリで`pnpm run build`コマンドを実行し、`dist`ディレクトリが生成されていることを確認します。

#### **2-2. Djangoの静的ファイル設定**

- `myproject/settings.py`を開き、以下の設定が正しく記述されていることを確認します。

```python
# myproject/settings.py

STATIC_URL = 
'/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/dist')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

---

### **ステップ3: Renderへのデプロイ**

1. **Renderにログイン**
   - ブラウザでRenderにアクセスし、GitHubアカウントでログインします。

2. **新しいWebサービスを作成**
   - ダッシュボードで「New +」→「Web Service」をクリックします。
   - 「Connect a repository」で、先ほど作成したGitHubリポジトリを選択します。

3. **Webサービスの設定**

| 設定項目 | 値 |
|---|---|
| **Name** | `fukushi-system`など、分かりやすい名前 |
| **Region** | Singapore (または最も近いリージョン) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && pnpm --prefix frontend install && pnpm --prefix frontend run build && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn myproject.wsgi` |
| **Instance Type** | Free |

4. **環境変数の設定**
   - 「Advanced」をクリックして、環境変数を設定します。

| キー | 値 |
|---|---|
| `PYTHON_VERSION` | `3.11.0` |
| `DATABASE_URL` | （ステップ4で作成するデータベースのURL） |
| `SECRET_KEY` | （新しいシークレットキーを生成して設定） |
| `OPENAI_API_KEY` | （あなたのOpenAI APIキー） |

5. **「Create Web Service」をクリック**
   - 初回デプロイが自動的に開始されます。（データベース設定がまだなので、一度失敗します）

---

### **ステップ4: PostgreSQLデータベースの作成と連携**

1. **新しいデータベースを作成**
   - Renderのダッシュボードで「New +」→「PostgreSQL」をクリックします。
   - **Name**: `fukushi-db`など、分かりやすい名前を入力します。
   - **Region**: Webサービスと同じリージョンを選択します。
   - 「Create Database」をクリックします。

2. **データベースURLの取得**
   - データベースのダッシュボードで、「Connections」セクションにある「Internal Database URL」をコピーします。

3. **WebサービスにデータベースURLを設定**
   - Webサービスのダッシュボードに戻り、「Environment」タブを開きます。
   - `DATABASE_URL`の値を、先ほどコピーしたInternal Database URLに書き換えます。
   - 「Save Changes」をクリックします。

4. **手動で再デプロイ**
   - Webサービスのダッシュボードで、「Manual Deploy」→「Deploy latest commit」をクリックします。
   - ビルドとデプロイが再度実行されます。

---

### **ステップ5: 動作確認**

1. **デプロイ完了の確認**
   - デプロイが完了すると、WebサービスのURLが発行されます。

2. **マイグレーションの実行**
   - Webサービスの「Shell」タブを開き、以下のコマンドを実行します。
   ```bash
   python manage.py migrate
   ```

3. **スーパーユーザーの作成**
   - 同様に「Shell」タブで、以下のコマンドを実行して管理者アカウントを作成します。
   ```bash
   python manage.py createsuperuser
   ```

4. **アプリケーションへのアクセス**
   - 発行されたURLにアクセスし、アプリケーションが正常に動作することを確認します。
   - 管理者アカウントでログインし、ダッシュボードが表示されることを確認します。

---

## 💡 トラブルシューティング

- **ビルドエラー**: `Build Command`が正しいか確認してください。
- **アプリケーションエラー**: Webサービスの「Logs」タブでエラーログを確認してください。
- **静的ファイルが表示されない**: `STATIC_ROOT`と`STATICFILES_DIRS`の設定を確認してください。

## ✅ 作業終了後の確認

- **ログアウト**: GitHubとRenderから必ずログアウトしてください。
- **ファイルの削除**: ダウンロードしたファイルや作成したファイルをPCから完全に削除してください。

これで、ネットカフェでのデプロイ作業は完了です！お疲れさまでした。
