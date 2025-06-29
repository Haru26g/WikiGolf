import wikipediaapi
from gensim.models import KeyedVectors
import collections

class WikiGolfer:
    """
    Wikipediaページ間の経路を探索する機能を提供するクラス。
    """
    def __init__(self, user_agent, model_path):
        """
        WikiGolferのインスタンスを初期化します。
        """
        self.wiki_api = wikipediaapi.Wikipedia(user_agent, 'ja')
        self.model = self._load_model(model_path)

    def _load_model(self, model_path):
        """
        指定されたパスからWord2Vecモデルをロードします。
        """
        try:
            print("モデルを読み込んでいます... (これには数分かかる場合があります)")
            model = KeyedVectors.load_word2vec_format(model_path, binary=False)
            print("モデルの読み込みが完了しました。")
            return model
        except FileNotFoundError:
            print(f"エラー: モデルファイルが見つかりません: {model_path}")
            exit()

    def find_path(self, start_title, goal_title, max_depth=50, branching_factor=10):
        """
        開始ページから目的ページへの経路を幅優先探索（BFS）で探します。

        Args:
            start_title (str): 開始ページのタイトル。
            goal_title (str): 目的ページのタイトル。
            max_depth (int): 探索する最大の深さ。
            branching_factor (int): 各ノードからキューに追加する最大ページ数。

        Returns:
            list[str] or None: 発見した経路のリスト。見つからない場合はNone。
        """
        start_page = self.wiki_api.page(start_title)
        if not start_page.exists():
            print(f"エラー: 開始ページ '{start_title}' が見つかりません。")
            return None

        goal_page = self.wiki_api.page(goal_title)
        if not goal_page.exists():
            print(f"エラー: 目的ページ '{goal_title}' が見つかりません。")
            return None

        # (page_object, path_list) をキューに積む
        queue = collections.deque([(start_page, [start_page.title])])
        visited = {start_page.title}

        print(f"\n探索開始: {start_page.title} -> {goal_page.title}")

        while queue:
            current_page, path = queue.popleft()

            # 現在の深さを表示
            print(f"探索中 (深さ {len(path)}): {current_page.title}")

            if len(path) > max_depth:
                print(f"-> 深さ制限 ({max_depth}) に達したため、この経路の探索を中止します。")
                continue

            links = current_page.links
            if not links:
                continue

            # ゴールが直接リンクに含まれているかチェック
            if goal_page.title in links:
                final_path = path + [goal_page.title]
                print(f"ゴールに到達しました！ ステップ数: {len(final_path) - 1}")
                return final_path

            # リンク先のページを類似度でソート
            candidates = []
            for title, page in links.items():
                if title not in visited:
                    try:
                        similarity = self.model.similarity(goal_page.title, title)
                        candidates.append((similarity, page))
                    except KeyError:
                        # モデルの語彙にない単語は無視
                        continue

            candidates.sort(key=lambda x: x[0], reverse=True)

            # 類似度の高い上位ページ（branching_factorで指定した数）をキューに追加する
            for sim, next_page in candidates[:branching_factor]:
                if next_page.title not in visited:
                    visited.add(next_page.title)
                    new_path = path + [next_page.title]
                    queue.append((next_page, new_path))

        return None # 経路が見つからなかった場合

def main():
    """
    ターミナルでユーザーからの入力を受け付け、WikiGolfを実行するメイン関数。
    """
    email_address = input("ユーザーエージェント用のメールアドレスを入力してください: ")
    user_agent = f'WikiShortestPath ({email_address})'
    model_path = r'C:\Users\Owner\MyPython\source code\WikiGolf\jawiki.all_vectors.100d.txt'

    golfer = WikiGolfer(user_agent, model_path)

    while True:
        start_input = input("\nStartページを入力してください (終了するにはEnterキーのみ): ")
        if not start_input:
            print("プログラムを終了します。")
            break

        goal_input = input("Goalページを入力してください: ")
        if not goal_input:
            continue

        path = golfer.find_path(start_input, goal_input)

        if path:
            print("\n--- 発見した経路 ---")
            print(" → ".join(path))
            print("--------------------\n")
        else:
            print("\n--- 経路が見つかりませんでした ---\n")

if __name__ == "__main__":
    main()